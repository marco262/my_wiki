from collections import defaultdict, OrderedDict
from glob import glob
from json import loads, load, dump
from os.path import splitext, basename, isfile

import toml
from bottle import view, request, HTTPError, Bottle, redirect

from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
from src.common.utils import str_to_bool, md_page, title_to_page_name
from src.dnd.search import Search
from src.dnd.utils import class_spell

SPELLS = {}
SEARCH_OBJ = Search()


def init():
    pass


def load_spells():
    global SPELLS
    if SPELLS:
        return SPELLS
    spells = {}
    path = None
    print("Loading spells into memory", end='')
    try:
        for path in glob("data/dnd/spell/*"):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd")
            spells[splitext(basename(path))[0]] = d
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    SPELLS = spells
    return SPELLS


def get_characters():
    path = "data/dnd/characters.json"
    if not isfile(path):
        return {}
    else:
        with open(path) as f:
            return load(f)


def save_characters(json):
    with open("data/dnd/characters.json") as f:
        dump(json, f)


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("5e Wiki", "dnd", build_toc=False)

    # Categories

    def get_md_page(category, name):
        formatted_name = title_to_page_name(name)
        path = f"data/dnd/{category}/{formatted_name}.md"
        try:
            md = MD.parse_md_path(path, namespace="dnd")
        except FileNotFoundError:
            raise HTTPError(404, f"I couldn't find \"{name}\".")
        if md.startswith("<p>REDIRECT "):
            redirect(md[12:-5])
        else:
            return {"title": name.title(), "text": md, "toc": md.toc_html}

    @app.get('/advancement/<name>')
    @view("common/page.tpl")
    def advancement(name):
        return get_md_page("advancement", name)

    @app.get('/background/<name>')
    @view("common/page.tpl")
    def background(name):
        return get_md_page("background", name)

    @app.get('/class/<name>')
    @view("common/page.tpl")
    def dnd_class(name):
        return get_md_page("class", name)

    @app.get('/equipment/<name>')
    @view("common/page.tpl")
    def equipment(name):
        return get_md_page("equipment", name)

    @app.get('/general/<name>')
    @view("common/page.tpl")
    def general(name):
        return get_md_page("general", name)

    @app.get('/monster/<name>')
    @view("common/page.tpl")
    def monster(name):
        return get_md_page("monster", name)

    @app.get('/race/<name>')
    @view("common/page.tpl")
    def race(name):
        return get_md_page("race", name)

    @app.get('/spell/<name>')
    @view("dnd/spell.tpl")
    def spell(name):
        formatted_name = title_to_page_name(name)
        loaded_spells = load_spells()
        if formatted_name not in loaded_spells:
            raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
        return loaded_spells[formatted_name]

    # Misc Functions

    @app.get('/search')
    @view('dnd/search.tpl')
    def search():
        return {}

    @app.route('/search/<search_term>')
    @view('dnd/search.tpl')
    def search_with_results(search_term):
        return {"search_key": search_term, "search_results": SEARCH_OBJ.run(search_term)}

    @app.get('/find_spell')
    @view('dnd/find_spell.tpl')
    def find_spell():
        return

    @app.get('/search_results/<search_key>')
    @view("dnd/spell_list_table.tpl")
    def search_results(search_key):
        results = []
        for k, v in load_spells().items():
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
        for k, v in load_spells().items():
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
            for t in filter_keys["durations"]:
                if t in v["duration"]:
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
                (filter_keys["expensive"] == "no" and v("expensive_material_component"))):
                continue
            if ((filter_keys["consumed"] == "yes" and not v.get("material_component_consumed")) or
                (filter_keys["consumed"] == "no" and v.get("material_component_consumed"))):
                continue
            results[v["level"]].append((k, v))
        d = {
            "spell_dict": results,
            "show_classes": len(filter_keys["classes"]) > 1,
            "ua_spells": filter_keys["ua_spells"]
        }
        return d

    @app.get('/all_spells_by_name/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def all_spells_by_name(ua_spells):
        spells = defaultdict(list)
        for k, v in load_spells().items():
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
        for k, v in load_spells().items():
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
        for k, v in load_spells().items():
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
        for k, v in load_spells().items():
            if v["ritual_spell"]:
                spells[v["level"]].append((k, v))
        d = {
            "title": "Ritual Spells",
            "spell_dict": spells,
            "show_classes": True,
            "ua_spells": str_to_bool(ua_spells)
        }
        return d

    @app.get('/characters')
    @view("dnd/characters.tpl")
    def characters():
        path = "data/dnd/characters.json"
        if not isfile(path):
            dnd_characters = None
        else:
            with open(path) as f:
                dnd_characters = load(f)
        return {"title": "Characters", "characters": dnd_characters}

    @app.get('/character/<name>')
    @view("dnd/character.tpl")
    def character(name):
        characters = get_characters()
        if name not in characters:
            raise HTTPError(404, f"I couldn't find any character named \"{name}\".")
        return {"name": characters[name]["name"], "json": characters[name]}

    @app.post('/save_character/<name>')
    @view("dnd/character.tpl")
    def save_character(name):
        characters = get_characters()
        characters[name] = loads(request.params["character_data"])
        save_characters(characters)
