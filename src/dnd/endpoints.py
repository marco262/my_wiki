import sys
import tomllib
from collections import defaultdict
from glob import glob
from json import loads
from os.path import splitext, basename

from bottle import Bottle, view, request

from src.common.utils import md_page, title_to_page_name

SPELLS = None
SPELLS_BY_LEVEL = None


def init(cfg):
    pass


def load_spells():
    global SPELLS, SPELLS_BY_LEVEL
    if SPELLS:
        return SPELLS
    SPELLS_BY_LEVEL = defaultdict(list)
    spells = {}
    path = None
    print("Loading spells into memory", end='')
    from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
    try:
        for path in sorted(glob("data/dnd/spell/*.toml")):
            print(".", end='', flush=True)
            with open(path, "rb") as f:
                d = tomllib.loads(f.read().decode())
            k = splitext(basename(path))[0]
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd", with_metadata=False)
            if "at_higher_levels" in d:
                d["at_higher_levels_md"] = MD.parse_md(
                    d["at_higher_levels"], namespace="dnd", with_metadata=False, no_p=True
                )
            if "at_higher_levels_homebrew" in d:
                d["at_higher_levels_homebrew_md"] = MD.parse_md(
                    d["at_higher_levels_homebrew"], namespace="dnd", with_metadata=False, no_p=True
                )
            if "source_extended" in d:
                d["source_extended"] = MD.parse_md(d["source_extended"], namespace="dnd", with_metadata=False)
            spells[k] = d
            SPELLS_BY_LEVEL[d["level"]].append((k, d))
    except Exception as e:
        raise Exception(f"Error when trying to process {path}") from e
    print(" Done.", flush=True)
    SPELLS = spells
    return SPELLS


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("2024 D&D Wiki", "dnd", build_toc=False)

    # Categories

    @app.get('/advancement/<name>')
    def advancement(name):
        return md_page(name, "dnd", "advancement")

    @app.get('/background/<name>')
    def background(name):
        return md_page(name, "dnd", "background")

    @app.get('/class/<name>')
    def dnd_class(name):
        return md_page(name, "dnd", "class")

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "dnd", "general")

    @app.get('/race/<name>')
    def race(name):
        return md_page(name, "dnd", "race")

    @app.get('/subclass/<name>')
    def subclass(name):
        return md_page(name, "dnd", "subclass")

    @app.get('/spell/<name>')
    @view("dnd/spell.tpl")
    def spell(name):
        formatted_name = title_to_page_name(name)
        loaded_spells = load_spells()
        return loaded_spells[formatted_name]

    @app.get('/spell_list/<c>')
    @view("dnd/spell_list_page.tpl")
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
    @view("dnd/spell_filter.tpl")
    def spell_filter():
        return

    @app.post('/spell_filter_results')
    @view("dnd/spell_list.tpl")
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
