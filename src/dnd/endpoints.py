import random
import re
from collections import defaultdict, OrderedDict
from glob import glob
from json import loads, load
from os.path import join as pjoin
from os.path import splitext, basename, isfile
from time import time

import bcrypt
from bottle import view, request, HTTPError, Bottle, template, redirect, auth_basic

from data.dnd.enums import spell_classes
from src.common import utils
from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
from src.common.utils import str_to_bool, md_page, title_to_page_name
from src.dnd.search import Search
from src.dnd.utils import init_spells_and_magic_items, class_spell, open_monster_sheet, load_spells, \
    load_spells_by_level, load_magic_items, get_magic_item_table, get_magic_item_subtypes, filter_magic_items

# Default password: dancinglikeastripper
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"
SEARCH_OBJ = Search()


def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")
    init_spells_and_magic_items()


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("5e Wiki", "dnd", build_toc=False)

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

    @app.get('/equipment/<name>')
    def equipment(name):
        return md_page(name, "dnd", "equipment")

    @app.get('/equipment/magic-item/<name>')
    @view("dnd/magic-item.tpl")
    def magic_item(name):
        formatted_name = title_to_page_name(name)
        loaded_magic_items = load_magic_items()
        if formatted_name not in loaded_magic_items:
            raise HTTPError(404, f"I couldn't find a magic item by the name of \"{name}\".")
        return loaded_magic_items[formatted_name]

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "dnd", "general")

    @app.get('/race/<name>')
    def race(name):
        return md_page(name, "dnd", "race")

    @app.get('/subclass/<name>')
    def subclass(name):
        return md_page(name, "dnd", "subclass")

    @app.get('/dm_toolbox/<name>')
    def subclass(name):
        return md_page(name, "dnd", "dm_toolbox")

    @app.get('/monster/<name>')
    def monster(name):
        return open_monster_sheet(name)

    @app.get('/spell/<name>')
    @view("dnd/spell.tpl")
    def spell(name):
        formatted_name = title_to_page_name(name)
        loaded_spells = load_spells()
        if formatted_name not in loaded_spells:
            raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
        return loaded_spells[formatted_name]

    # Misc Functions

    @app.get('/site_search')
    @view('dnd/site_search.tpl')
    def site_search():
        return {
            "title": "Search",
            "include_search_box": True,
        }

    @app.route('/site_search/<search_term>')
    @view('dnd/site_search.tpl')
    def site_search_with_results(search_term):
        t = time()
        results = SEARCH_OBJ.run(search_term)
        results_per_page = 10
        total_pages = len(results) // results_per_page + 1 if results is not None else 1
        try:
            page = max(0, min(total_pages, int(request.params["page"])))
        except (ValueError, KeyError):
            page = 1
        if total_pages > 1:
            results = results[(page - 1) * results_per_page:page * results_per_page]
        return {
            "title": "Search",
            "search_key": search_term,
            "search_results": results,
            "processing_time": time() - t,
            "page": page,
            "total_pages": total_pages,
            "results_per_page": results_per_page,
            "include_search_box": True,
        }

    # Intended for use as a browser bookmark for quickly searching for any specific page
    @app.route("/page_search/<search_term>")
    def page_search_with_results(search_term):
        t = time()
        results = SEARCH_OBJ.page_search(search_term)
        if isinstance(results, list):
            return template(
                "dnd/site_search.tpl",
                title="Page Search",
                search_key=search_term,
                search_results=results,
                processing_time=time() - t,
                include_search_box=False
            )
        else:
            # results is not a list, but a URI we should redirect to
            redirect(results)

    @app.get('/find_spell')
    @view('dnd/find_spell.tpl')
    def find_spell():
        return

    @app.get('/search_results/<search_key>')
    @view("dnd/spell_list_table.tpl")
    def search_results(search_key):
        results = []
        search_key = search_key.lower()
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

    @app.post('/spell_filter_results')
    @view("dnd/spell_list.tpl")
    def spell_filter_results():
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
        d = {
            "spell_dict": results,
            "show_classes": len(filter_keys["classes"]) > 1,
            "ua_spells": filter_keys["ua_spells"]
        }
        return d

    @app.get("/equipment/magic_item_filter/")
    @view("dnd/magic_item_filter.tpl")
    def magic_item_filter():
        return {"subtypes": get_magic_item_subtypes()}

    @app.post('/equipment/magic_item_filter_results')
    @view("dnd/magic-items.tpl")
    def magic_item_filter_results():
        filter_keys = loads(request.params["filter_keys"])
        filtered_magic_items = filter_magic_items(filter_keys)
        results = defaultdict(list)
        for k, v in filtered_magic_items.items():
            results[v["rarity"]].append((k, v))
        return {"magic_items": results}

    @app.get("/equipment/magic_item_generator/")
    @view("dnd/magic_item_generator.tpl")
    def magic_item_generator():
        return {"subtypes": get_magic_item_subtypes()}

    @app.post("/equipment/magic_item_generator_results/")
    def magic_item_generator_results():
        d = {
            "A": ("Minor", "Common"),
            "B": ("Minor", "Uncommon"),
            "C": ("Minor", "Rare"),
            "D": ("Minor", "Very Rare"),
            "E": ("Minor", "Legendary"),
            "F": ("Major", "Uncommon"),
            "G": ("Major", "Rare"),
            "H": ("Major", "Very Rare"),
            "I": ("Major", "Legendary"),
        }
        table_type = d.get(request.params["table_name"].upper())
        if not table_type:
            return HTTPError(status=406, body=f'No magic item table {request.params["table_name"]}')
        rarity_type, rarity = table_type
        filter_keys = loads(request.params["filter_keys"])
        filtered_magic_items = filter_magic_items(filter_keys)
        table = get_magic_item_table(filtered_magic_items, rarity_type, rarity)
        items_with_weights = list(table.items())
        if not items_with_weights:
            return MD.parse_md("*No items matched your filter.*")
        _, weights = zip(*items_with_weights)
        spells_by_level = load_spells_by_level()
        output = "\n"
        for _ in range(int(request.params["max_items"])):
            magic_item_tuple = random.choices(items_with_weights, weights=weights, k=1)[0]
            magic_item = magic_item_tuple[0]
            m = re.search(r"(.*) \(.*\)$", magic_item)
            if m:
                page_name = m.group(1)
            else:
                page_name = magic_item
            output += f"* [{magic_item}](/dnd/equipment/magic-item/{page_name})"
            # Add random spell to the end of the item name if necessary
            m = re.search(r"(?:Spell Scroll|Spellwrought Tattoo), (.+)$", magic_item)
            if m:
                level = "cantrip" if m.group(1) == "Cantrip" else m.group(1)[0]
                _, random_spell = random.choice(spells_by_level[level])
                output += f" (_[[[spell:{random_spell['title'].lower()}]]]_)"
            else:
                # If it's not a spell scroll or tattoo, and we want to avoid duplicates, remove the chosen item from set
                if request.params["no_duplicates"] == "true":
                    items_with_weights.remove(magic_item_tuple)
                    if len(items_with_weights) == 0:
                        break
                    _, weights = zip(*items_with_weights)
            output += "\n"
        return MD.parse_md(output, namespace="dnd")

    @app.get('/all_spells_by_name/<ua_spells>')
    @view("dnd/spell_list_page.tpl")
    def all_spells_by_name(ua_spells):
        spells = load_spells_by_level()
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
        dnd_characters = []
        for path in sorted(glob("data/dnd/characters/*.json")):
            dnd_characters.append(splitext(basename(path))[0])
        return {"title": "Characters", "characters": dnd_characters}

    @app.get('/character/<name>')
    @view("dnd/character.tpl")
    def character(name):
        path = "data/dnd/characters/{}.json".format(name)
        if not isfile(path):
            raise HTTPError(404, f"I couldn't find any character named \"{name}\".")
        with open(path) as f:
            dnd_character = load(f)
        return {"title": name, "json": dnd_character}

    @app.post('/save_character/<name>')
    @view("dnd/character.tpl")
    def save_character(name):
        with open("data/dnd/character/{}.json".format(name), 'w') as f:
            f.write(request.params["character_data"])

    @app.get("/gm/monsters_by_name")
    @view("dnd/monsters-by-name.tpl")
    def monsters_by_name():
        folder = "data/dnd/monster"
        file_paths = sorted(glob(pjoin(folder, "*")))
        monsters = OrderedDict()
        excluded_files = ["all-pages.md", "include_monster-sheet.txt"]
        excluded_files = [pjoin(folder, f) for f in excluded_files]
        for path in file_paths:
            if path in excluded_files:
                continue
            filename = splitext(basename(path))[0]
            link = "/dnd/monster/" + filename
            name = filename.replace("-", " ").title()
            # Don't overwrite *.md entries with *.toml entries
            if path.endswith("*.toml") and name in monsters:
                continue
            monsters[name] = link
        return {"monsters": monsters}

    @app.get("gm_notes/insert/<name>")
    @auth_basic(gm_notes_auth_check)
    def gm_notes_insert(name):
        return md_page(name, "dnd", directory="gm_notes/inserts", load_template=False)


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
