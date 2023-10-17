from collections import defaultdict, OrderedDict
from glob import glob
from os.path import splitext, basename

import toml
from bottle import Bottle, view, redirect

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
        for path in sorted(glob("data/onednd/spell/*")):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd")
            if "source_extended" in d:
                d["source_extended"] = MD.parse_md(d["source_extended"], namespace="dnd")
            k = splitext(basename(path))[0]
            spells[k] = d
            SPELLS_BY_LEVEL[d["level"]].append((k, d))
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    SPELLS = spells
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
