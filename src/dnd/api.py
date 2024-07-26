import json

from bottle import HTTPError, Bottle, request, FormsDict

from data.dnd.enums import spell_classes
from src.common.utils import title_to_page_name
from src.dnd.utils import load_spells, filter_magic_items, load_magic_items, get_magic_item_subtypes


def load_api_endpoints(app: Bottle):

    @app.get("/spell_list")
    def get_full_spell_list():
        return get_spell_list()

    @app.get("/spell_list/<spell_class>")
    def get_class_spell_list(spell_class):
        return get_spell_list(spell_class)

    @app.get("/spell_list/<spell_class>/<level>")
    def get_class_spell_list_level(spell_class, level):
        return get_spell_list(spell_class, level)

    @app.get("/spell/<name>")
    def get_class_spell(name):
        formatted_name = title_to_page_name(name)
        spells = load_spells()
        if formatted_name not in spells:
            raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
        return spells[formatted_name]

    @app.get("/magic_items")
    def get_magic_items():
        return get_magic_item_list(request.query)

    @app.get("/magic_items/subtypes")
    def get_magic_item_subtypes_api():
        return json.dumps(get_magic_item_subtypes())

    @app.get("/magic_item/<name>")
    def get_magic_item(name):
        formatted_name = title_to_page_name(name)
        magic_items = load_magic_items()
        if formatted_name not in magic_items:
            raise HTTPError(404, f"I couldn't find a magic item by the name of \"{name}\".")
        return magic_items[formatted_name]


def get_spell_list(name: str = "", level: str = "") -> str:
    spells = load_spells()
    if name not in ("", "all"):
        name = name.lower()
        # Get spell lists by class
        if name not in spell_classes:
            raise HTTPError(404, f'"{name}" is not a valid spell list.')
        spells = {k: v for k, v in spells.items() if name in v["classes"]}
        # If no level, return list
        if level != "":
            level = level.lower()
            # Filter more by level
            if not (level == "cantrip" or (level.isdigit() and 0 <= int(level) <= 9)):
                raise HTTPError(404, f'"{level}" is not a valid spell level.')
            if level == "0":
                level = "cantrip"
            spells = {k: v for k, v in spells.items() if level == v["level"]}
    return json.dumps(list(spells.keys()))


def get_magic_item_list(query: FormsDict) -> str:
    # Convert comma-delimited strings in values to lists
    filters = {}
    for k, v in query.items():
        filters[k] = v.split(",")
    print(filters)
    magic_items = filter_magic_items(filters)
    return json.dumps(list(magic_items.keys()))
