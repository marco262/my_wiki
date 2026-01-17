from collections import defaultdict
from json import loads
from time import perf_counter

from bottle import Bottle, view, request, redirect, abort, template

from src.common.utils import md_page, title_to_page_name
from src.dnd.search import Search
from src.dnd.utils import load_spells, open_monster_sheet

SEARCH_OBJ = None


def init(_cfg):
    pass


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

    @app.get('/dm/<name>')
    def dnd_class(name):
        return md_page(name, "dnd", "dm")

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "dnd", "general")

    @app.get('/monster/<name>')
    def race(name):
        return open_monster_sheet(name)

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
        if formatted_name in loaded_spells:
            return loaded_spells[formatted_name]
        else:
            abort(404, f"Could not find spell '{name}'")
        return None

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

    # Misc Functions

    @app.get('/site_search')
    @view('dnd5e/site_search.tpl')
    def site_search():
        return {
            "title": "Search",
            "include_search_box": True,
        }

    @app.route('/site_search/<search_term>')
    @view('dnd5e/site_search.tpl')
    def site_search_with_results(search_term):
        global SEARCH_OBJ
        t = perf_counter()
        if not SEARCH_OBJ:
            SEARCH_OBJ = Search()
        results = SEARCH_OBJ.run(search_term, "dnd")
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
            "processing_time": perf_counter() - t,
            "page": page,
            "total_pages": total_pages,
            "results_per_page": results_per_page,
            "include_search_box": True,
        }

    # Intended for use as a browser bookmark for quickly searching for any specific page
    @app.route("/page_search/<search_term>")
    def page_search_with_results(search_term):
        global SEARCH_OBJ
        t = perf_counter()
        if not SEARCH_OBJ:
            SEARCH_OBJ = Search()
        results = SEARCH_OBJ.page_search(search_term, "dnd")
        if isinstance(results, list):
            return template(
                "dnd/site_search.tpl",
                title="Page Search",
                search_key=search_term,
                search_results=results,
                processing_time=perf_counter() - t,
                include_search_box=False
            )
        else:
            # results is not a list, but a URI we should redirect to
            redirect(results)
