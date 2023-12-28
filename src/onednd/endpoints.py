from collections import defaultdict, OrderedDict
from copy import deepcopy
from glob import glob
from json import loads
from os.path import splitext, basename

import toml
from bottle import Bottle, view, redirect, request

from src.common.utils import md_page, title_to_page_name
from src.dnd.utils import load_spells as load_core_spells

SPELLS = None
SPELLS_BY_LEVEL = None


def init(cfg):
    pass


def load_spells():
    global SPELLS, SPELLS_BY_LEVEL
    if SPELLS:
        return SPELLS
    SPELLS_BY_LEVEL = defaultdict(list)
    core_spells = deepcopy(load_core_spells())
    spells = {}
    path = None
    print("Loading spells into memory", end='')
    from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
    try:
        for path in sorted(glob("data/onednd/spell/*.toml")):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            k = splitext(basename(path))[0]
            if k in core_spells:
                d["spell_lists"] = set(d["spell_lists"]).union([c.title() for c in core_spells[k]["classes"]])
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd")
            if "source_extended" in d:
                d["source_extended"] = MD.parse_md(d["source_extended"], namespace="dnd")
            spells[k] = d
            SPELLS_BY_LEVEL[d["level"]].append((k, d))
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    for _, v in core_spells.items():
        v["spell_lists"] = [c.title() for c in v["classes"]]
        v["school"] = v["school"].title()
        if v["level"] == "cantrip":
            v["level"] = "0"
        if v["casting_time"] == "1 action":
            v["casting_time"] = "Action"
        elif v["casting_time"] == "1 bonus action":
            v["casting_time"] = "Bonus Action"
        elif v["casting_time"].startswith("1 reaction"):
            v["casting_time"] = v["casting_time"].replace("1 reaction", "Reaction")
    core_spells.update(spells)
    SPELLS = core_spells
    return SPELLS


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("One D&D Wiki", "onednd", build_toc=False)

    # Categories

    @app.get('/advancement/<name>')
    def advancement(name):
        return md_page(name, "onednd", "advancement")

    @app.get('/class/<name>')
    def dnd_class(name):
        return md_page(name, "onednd", "class")

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "onednd", "general")

    @app.get('/race/<name>')
    def race(name):
        return md_page(name, "onednd", "race", build_toc=False)

    @app.get('/subclass/<name>')
    def subclass(name):
        return md_page(name, "onednd", "subclass")

    @app.get('/spell/<name>')
    @view("onednd/spell.tpl")
    def spell(name):
        formatted_name = title_to_page_name(name)
        loaded_spells = load_spells()
        if formatted_name not in loaded_spells:
            redirect(f"/dnd/spell/{name}")
            return
        return loaded_spells[formatted_name]

    @app.get('/spell_list/<c>')
    @view("onednd/spell_list_page.tpl")
    def class_spell_list(c):
        c = c.title()
        spells = defaultdict(list)
        for k, v in load_spells().items():
            if c in v["spell_lists"]:
                spells[v["level"]].append((k, v))
        # Sort results by name
        for k, spell_list in spells.items():
            spells[k] = sorted(spell_list, key=lambda x: x[0])
        d = {
            "title": f"{c.title()} Spells",
            "spell_dict": spells,
            "show_classes": False
        }
        return d

    @app.get("/spell_filter")
    @view("onednd/spell_filter.tpl")
    def spell_filter():
        return

    @app.post('/spell_filter_results')
    @view("onednd/spell_list.tpl")
    def spell_filter_results():
        filter_keys = loads(request.params["filter_keys"])
        results = defaultdict(list)
        spells = load_spells()
        for k, v in spells.items():
            if not set(filter_keys["spell_lists"]).intersection(v["spell_lists"]):
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
            for t in filter_keys["ranges"]:
                if t in v["range"]:
                    break
            else:
                continue
            for d in filter_keys["durations"]:
                if d in v["duration"]:
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
            if ((filter_keys["expensive"] == "yes" and not v.get("expensive_material_component")) or
                    (filter_keys["expensive"] == "no" and v.get("expensive_material_component"))):
                continue
            if ((filter_keys["consumed"] == "yes" and not v.get("material_component_consumed")) or
                    (filter_keys["consumed"] == "no" and v.get("material_component_consumed"))):
                continue
            results[v["level"]].append((k, v))
        # Sort results by name
        for k, spell_list in results.items():
            results[k] = sorted(spell_list, key=lambda x: x[0])
        d = {
            "spell_dict": results,
            "show_classes": len(filter_keys["spell_lists"]) > 1
        }
        return d
