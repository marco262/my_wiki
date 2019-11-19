import os
import re
from collections import OrderedDict, defaultdict
from glob import glob
from json import loads
from os.path import basename, splitext

import markdown2
import toml
from bottle import get, run, view, route, static_file, HTTPError
from fasteners import process_lock

from utils import setup_logging, load_config, str_to_bool

VERSION = (0, 0, 1)
VIEWS_DIR = os.path.join(os.path.dirname(__file__), 'views')
RESOURCES_DIR = os.path.join(os.path.dirname(__file__), 'resources')


class Server:
    """
    On load:
     - Check if any other server instances are running, fail if so.
     - Establish logging to the server.log file. Redirect stderr to this log file, to catch the output thrown
       by the Bottle server.
     - Load the WSGI functions.
     - Start the Bottle server.
    """

    server_thread = None
    interval = None

    def __init__(self, host=None, port=None, log_level=None, run_as_thread=None):
        self._get_process_lock()

        cfg = load_config()
        self.logger = setup_logging("log", log_level=log_level)
        self.md = markdown2.Markdown()

        self._load_spells()

        self._load_wsgi_functions()
        self._init_server(
            host=cfg.get("Settings", "host") if host is None else host,
            port=cfg.getint("Settings", "port") if port is None else port,
            run_as_thread=cfg.getboolean("Settings", "run as thread") if run_as_thread is None else run_as_thread
        )

    @staticmethod
    def _get_process_lock():
        lock = process_lock.InterProcessLock("server.lock")
        if not lock.acquire(blocking=False):
            raise ChildProcessError("Server process is already running")

    def _init_server(self, host=None, port=None, run_as_thread=None):
        if run_as_thread:
            from threading import Thread
            self.server_thread = Thread(name="MyWikiServer", target=self._run_server, args=[host, port],
                                        daemon=True)
            self.server_thread.start()
            print("Server thread started.")
        else:
            self._run_server(host, port)

    @staticmethod
    def _run_server(host, port):
        run(host=host, port=port)
        print("Server instance is ending.")

    def _load_spells(self):
        path = None
        self.spells = {}
        print("Loading spells into memory", end='')
        try:
            for path in glob("data/spell/*"):
                print(".", end='')
                with open(path) as f:
                    d = toml.loads(f.read(), _dict=OrderedDict)
                d["description_md"] = self.md.convert(d["description"])
                self.spells[splitext(basename(path))[0]] = d
        except Exception:
            print(f"\nError when trying to process {path}")
            raise
        print(" Done.")

    def _load_wsgi_functions(self):
        """
        Loads functions into the WSGI
        """
        @get('/')
        @get('/help')
        @view('home.tpl')
        def index_help():
            return

        @route("/static/:path#.+#", name="static")
        def static(path):
            return static_file(path, root="static")

        @get('/search')
        @view('search.tpl')
        def search():
            return

        @get('/search_results/<search_key>')
        @view("spell_list_table.tpl")
        def search_results(search_key):
            results = []
            for k, v in self.spells.items():
                if search_key in v['title'].lower():
                    results.append((k, v))
            d = {
                "spells": results,
                "show_classes": True
            }
            return d

        @get("/spell_filter")
        @view("spell_filter.tpl")
        def spell_filter():
            return

        @get('/filter_results/<json>')
        @view("spell_list.tpl")
        def filter_results(json):
            filter_keys = loads(json)
            results = defaultdict(list)
            for k, v in self.spells.items():
                if not (set(filter_keys["classes"]).intersection(v["classes"]) or
                        (filter_keys["ua_spells"] and set(filter_keys["classes"]).intersection(v.get("classes_ua", [])))
                ):
                    continue
                if not v["level"] in filter_keys["levels"]:
                    continue
                if not v["school"] in filter_keys["schools"]:
                    continue
                if ((filter_keys["concentration"] == "yes" and not v["concentration_spell"]) or
                    (filter_keys["concentration"] == "no" and v["concentration_spell"])):
                    continue
                if ((filter_keys["ritual"] == "yes" and not v["ritual_spell"]) or
                    (filter_keys["ritual"] == "no" and v["ritual_spell"])):
                    continue
                if ((filter_keys["verbal"] == "yes" and "V" not in v["components"]) or
                    (filter_keys["verbal"] == "no" and "V" in v["components"])):
                    continue
                if ((filter_keys["somatic"] == "yes" and "S" not in v["components"]) or
                    (filter_keys["somatic"] == "no" and "S" in v["components"])):
                    continue
                if ((filter_keys["material"] == "yes" and "M" not in v["components"]) or
                    (filter_keys["material"] == "no" and "M" in v["components"])):
                    continue
                if ((filter_keys["expensive"] == "yes" and not v["expensive_material_component"]) or
                    (filter_keys["expensive"] == "no" and v["expensive_material_component"])):
                    continue
                if ((filter_keys["consumed"] == "yes" and not v["material_component_consumed"]) or
                    (filter_keys["consumed"] == "no" and v["material_component_consumed"])):
                    continue
                results[v["level"]].append((k, v))
            d = {
                "spell_dict": results,
                "show_classes": len(filter_keys["classes"]) > 1,
                "ua_spells": filter_keys["ua_spells"]
            }
            return d

        @get('/spell/<name>')
        @view("spell.tpl")
        def spell(name):
            formatted_name = re.sub("\W", "-", name.lower())
            if formatted_name not in self.spells:
                raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
            return self.spells[formatted_name]

        @get('/all_spells_by_name/<ua_spells>')
        @view("spell_list_page.tpl")
        def all_spells_by_name(ua_spells):
            spells = defaultdict(list)
            for k, v in self.spells.items():
                spells[v["level"]].append((k, v))
            d = {
                "title": "All Spells By Name",
                "spell_dict": spells,
                "show_classes": True,
                "ua_spells": str_to_bool(ua_spells)
            }
            return d

        @get('/class_spell_list/<c>/<ua_spells>')
        @view("spell_list_page.tpl")
        def class_spell_list(c, ua_spells):
            spells = defaultdict(list)
            for k, v in self.spells.items():
                if (c.lower() in v["classes"] or
                        (str_to_bool(ua_spells) and c.lower() in v.get("classes_ua", []))):
                    spells[v["level"]].append((k, v))
            d = {
                "title": f"{c.title()} Spells",
                "spell_dict": spells,
                "show_classes": False
            }
            return d

        @get('/concentration_spells/<ua_spells>')
        @view("spell_list_page.tpl")
        def concentration_spell_list(ua_spells):
            spells = defaultdict(list)
            for k, v in self.spells.items():
                if v["concentration_spell"]:
                    spells[v["level"]].append((k, v))
            d = {
                "title": "Concentration Spells",
                "spell_dict": spells,
                "show_classes": True,
                "ua_spells": str_to_bool(ua_spells)
            }
            return d

        @get('/ritual_spells/<ua_spells>')
        @view("spell_list_page.tpl")
        def ritual_spell_list(ua_spells):
            spells = defaultdict(list)
            for k, v in self.spells.items():
                if v["ritual_spell"]:
                    spells[v["level"]].append((k, v))
            d = {
                "title": "Ritual Spells",
                "spell_dict": spells,
                "show_classes": True,
                "ua_spells": str_to_bool(ua_spells)
            }
            return d

        @get('/feedback')
        def feedback():
            return "Feedback here"


if __name__ == "__main__":
    Server()
