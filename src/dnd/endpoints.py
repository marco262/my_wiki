import re
from collections import defaultdict, OrderedDict
from glob import glob
from json import loads
from os.path import splitext, basename

import toml
from bottle import view, request, HTTPError, Bottle
from src import MD

from src.common.markdown_parser import MarkdownParser
from src.common.utils import str_to_bool, md_page
from src.dnd.utils import class_spell

SPELLS = {}


def init():
    load_spells()


def load_spells():
    global SPELLS
    path = None
    print("Loading spells into memory", end='')
    try:
        for path in glob("data/dnd/spell/*"):
            print(".", end='')
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description_md"] = MD.parse_md(d["description"])
            SPELLS[splitext(basename(path))[0]] = d
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.")


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("5e Wiki", "dnd", build_toc=False)

    @app.get('/search')
    @view('dnd/search.tpl')
    def search():
        return

    @app.get('/search_results/<search_key>')
    @view("dnd/spell_list_table.tpl")
    def search_results(search_key):
        results = []
        for k, v in SPELLS.items():
            if search_key in v['title'].lower():
                results.append((k, v))
        d = {
            "spells": results,
            "show_classes": True
        }
        return d

    @app.get("/spell_filter")
    @view("dnd/spell_filter.tpl")
    def spell_filter():
        return

    @app.post('/filter_results')
    @view("dnd/spell_list.tpl")
    def filter_results():
        filter_keys = loads(request.params["filter_keys"])
        results = defaultdict(list)
        for k, v in SPELLS.items():
            if not class_spell(v, filter_keys["classes"], filter_keys["ua_spells"]):
                continue
            if v["level"] not in filter_keys["levels"]:
                continue
            if v["school"] not in filter_keys["schools"]:
                continue
            for s in filter_keys["sources"]:
                if s in v["source"]:
                    break
            else:
                continue
            for t in filter_keys["casting_times"]:
                if t in v["casting_time"]:
                    break
            else:
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

    @app.get('/spell/<name>')
    @view("dnd/spell.tpl")
    def spell(name):
        formatted_name = re.sub(r"\W", "-", name.lower())
        if formatted_name not in SPELLS:
            raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
        return SPELLS[formatted_name]

    @app.get('/all_spells_by_name/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def all_spells_by_name(ua_spells):
        spells = defaultdict(list)
        for k, v in SPELLS.items():
            spells[v["level"]].append((k, v))
        d = {
            "title": "All Spells By Name",
            "spell_dict": spells,
            "show_classes": True,
            "ua_spells": str_to_bool(ua_spells)
        }
        return d

    @app.get('/class_spell_list/<c>/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def class_spell_list(c, ua_spells):
        spells = defaultdict(list)
        for k, v in SPELLS.items():
            if (c.lower() in v["classes"] or
                    (str_to_bool(ua_spells) and c.lower() in v.get("classes_ua", []))):
                spells[v["level"]].append((k, v))
        d = {
            "title": f"{c.title()} Spells",
            "spell_dict": spells,
            "show_classes": False
        }
        return d

    @app.get('/concentration_spells/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def concentration_spell_list(ua_spells):
        spells = defaultdict(list)
        for k, v in SPELLS.items():
            if v["concentration_spell"]:
                spells[v["level"]].append((k, v))
        d = {
            "title": "Concentration Spells",
            "spell_dict": spells,
            "show_classes": True,
            "ua_spells": str_to_bool(ua_spells)
        }
        return d

    @app.get('/ritual_spells/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def ritual_spell_list(ua_spells):
        spells = defaultdict(list)
        for k, v in SPELLS.items():
            if v["ritual_spell"]:
                spells[v["level"]].append((k, v))
        d = {
            "title": "Ritual Spells",
            "spell_dict": spells,
            "show_classes": True,
            "ua_spells": str_to_bool(ua_spells)
        }
        return d

    @app.get('/class/<name>')
    @view("dnd/class.tpl")
    def dnd_class(name):
        formatted_name = re.sub(r"\W", "-", name.lower())
        path = "data/dnd/class/" + formatted_name + ".md"
        try:
            md = MD.parse_md_path(path)
        except FileNotFoundError:
            raise HTTPError(404, f"I couldn't find \"{name}\".")
        return {"title": name.title(), "text": md, "toc": md.toc_html}
