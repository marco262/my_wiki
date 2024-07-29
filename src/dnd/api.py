import json
from copy import deepcopy

from bottle import HTTPError, Bottle, request

from src.common.utils import title_to_page_name
from src.dnd.utils import load_spells, filter_spells, load_magic_items, filter_magic_items, get_enum_cache


def load_api_endpoints(app: Bottle):

    @app.get("/spell_list")
    def get_spell_list():
        # Convert comma-delimited strings in values to lists
        filters = {}
        for k, v in request.query.items():
            filters[k] = v.split(",")
        spells, _ = filter_spells(filters)
        return json.dumps(list(spells.keys()))

    @app.get("/spell_list/enum")
    def get_spell_list_enum():
        return get_enum_cache("spell")

    @app.get("/spell/<name>")
    def get_spell(name):
        formatted_name = title_to_page_name(name)
        spells = load_spells()
        if formatted_name not in spells:
            raise HTTPError(404, f"I couldn't find a spell by the name of \"{name}\".")
        return spells[formatted_name]

    @app.get("/magic_items")
    def get_magic_items():
        # Convert comma-delimited strings in values to lists
        filters = {}
        for k, v in request.query.items():
            filters[k] = v.split(",")
        print(filters)
        magic_items = filter_magic_items(filters)
        return json.dumps(list(magic_items.keys()))

    @app.get("/magic_items/enum")
    def get_magic_item_enum():
        cache = deepcopy(get_enum_cache("magic_item"))
        # Add no-subtype option to subtype enums
        cache["subtype"].insert(0, "no-subtype")
        return cache

    @app.get("/magic_item/<name>")
    def get_magic_item(name):
        formatted_name = title_to_page_name(name)
        magic_items = load_magic_items()
        if formatted_name not in magic_items:
            raise HTTPError(404, f"I couldn't find a magic item by the name of \"{name}\".")
        return magic_items[formatted_name]
