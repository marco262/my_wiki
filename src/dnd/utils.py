from collections import OrderedDict
from enum import Enum
from glob import glob
from os.path import join as pjoin, isfile, splitext, basename
from typing import List, Optional, Union

import toml
from bottle import HTTPError, redirect, template

from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
from src.common.utils import md_page, title_to_page_name


class Mode(Enum):
    TITLE = "TITLE"
    BRIEF = "BRIEF"
    FULL = "FULL"


INCLUDE_MD = """[[include dnd/monster-sheet.tpl]]
file = {}
[[/include]]"""


def class_spell(spell: dict, classes: List[str], ua_spells: bool) -> bool:
    """
    Helper function for determining if a spell belongs to any of a list of classes
    :param spell: The parsed spell dictionary, containing classes and classes_ua fields
    :param classes: The list of classes to check against
    :param ua_spells: Whether or not to include the classes_ua field in the spell
    :return:
    """
    return bool(
        (set(classes).intersection(spell["classes"])) or
        (ua_spells and set(classes).intersection(spell.get("classes_ua", [])))
    )


def results_mode(d: dict, mode: Optional[str]) -> Union[str, dict]:
    """
    Takes in a spell dictionary (or other dict from a TOML file) and returns the contents based on the mode
    passed in. TITLE returns only the title. BRIEF returns everything but the description. FULL returns the full dict.
    :param d: dictionary of data
    :param mode: TITLE (or None), BRIEF, or FULL
    :return:
    """
    if mode is None:
        mode = Mode.TITLE
    if mode == Mode.TITLE.value:
        return d["title"]
    if mode == Mode.BRIEF.value:
        filter_keys = ["description", "at_higher_levels", "description_md"]
        filtered_dict = {}
        for k, v in d.items():
            if k not in filter_keys:
                filtered_dict[k] = v
        return filtered_dict
    if mode == Mode.FULL.value:
        return d
    raise ValueError(f"{mode} is not a valid results mode")


def ability_mod(score: Union[str, int, float]) -> str:
    return to_mod((int(score) - 10) / 2)


def to_mod(num):
    mod = str(int(num))
    if not mod.startswith("-"):
        mod = "+" + mod
    return mod


def open_monster_sheet(name):
    try:
        return md_page(name, "dnd", "monster", build_toc=False)
    except HTTPError:
        # If we can't find a template or MD file, check for a TOML file itself and just load the monster-sheet
        toml_path = pjoin("dnd/monster", title_to_page_name(name) + ".toml")
        if not isfile(pjoin("data", toml_path)):
            raise HTTPError(404, f"Can't find a page for \"/dnd/monster/{name}\"")
        toml_dict = toml.load(pjoin("data", toml_path))
        if "redirect" in toml_dict:
            return redirect(toml_dict["redirect"])
        md_text = MD.parse_md(INCLUDE_MD.format(toml_path), namespace="dnd")
        return template("common/page.tpl", {"title": toml_dict["name"], "text": md_text})


MAGIC_ITEMS = {}


def load_magic_items():
    global MAGIC_ITEMS
    if MAGIC_ITEMS:
        return MAGIC_ITEMS
    magic_items = {}
    path = None
    print("Loading magic items into memory", end='')
    try:
        for path in glob("data/dnd/equipment/magic-items/*"):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd")
            magic_items[splitext(basename(path))[0]] = d
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    MAGIC_ITEMS = magic_items
    return MAGIC_ITEMS


def get_magic_item_table(rarity_type, rarity):
    if rarity == "Common":
        rarity_type = "Minor"

    excluded_items = []
    if rarity == "Common":
        table = OrderedDict([
            ("Potion of Healing", 50),
            ("Spell Scroll, Cantrip", 10),
            ("Potion of Climbing", 10),
            ("Spell Scroll, 1st Level", 20),
            ("Spell Scroll, 2nd Level", 5),
            ("Potion of Greater Healing", 5),
            ("Bag of Holding", 2),
            ("Driftglobe", 2),
        ])
    elif rarity_type == "Minor" and rarity == "Uncommon":
        table = OrderedDict([
            ("Potion of Greater Healing", 15),
            ("Potion of Fire Breath", 7),
            ("Potion of Resistance", 7),
            ("Ammunition, +1", 5),
            ("Potion of Animal Friendship", 5),
            ("Potion of Hill Giant Strength", 5),
            ("Potion of Growth", 5),
            ("Potion of Water Breathing", 5),
            ("Spell Scroll, 2nd Level", 5),
            ("Spell Scroll, 3rd Level", 5),
            ("Bag of Holding", 3),
            ("Keoghtom's Ointment", 3),
            ("Oil of Slipperiness", 3),
            ("Dust of Disappearance", 2),
            ("Dust of Dryness", 2),
            ("Dust of Sneezing and Choking", 2),
            ("Elemental Gem", 2),
            ("Philter of Love", 2),
        ])
    elif rarity_type == "Minor" and rarity == "Rare":
        table = OrderedDict([
            ("Potion of Superior Healing", 15),
            ("Spell Scroll, 4th Level", 7),
            ("Ammunition, +2", 5),
            ("Potion of Clairvoyance", 5),
            ("Potion of Diminution", 5),
            ("Potion of Gaseous Form", 5),
            ("Potion of Frost Giant Strength", 5),
            ("Potion of Stone Giant Strength", 5),
            ("Potion of Heroism", 5),
            ("Potion of Invulnerability", 5),
            ("Potion of Mind Reading", 5),
            ("Spell Scroll, 5th Level", 5),
            ("Elixir of Health", 3),
            ("Oil of Etherealness", 3),
            ("Potion of Fire Giant Strength", 3),
            ("Quaal's Feather Token", 3),
            ("Scroll of Protection", 3),
            ("Bag of Beans", 2),
            ("Bead of Force", 2),
        ])
    elif rarity_type == "Minor" and rarity == "Very Rare":
        table = OrderedDict([
            ("Potion of Supreme Healing", 20),
            ("Potion of Invisibility", 10),
            ("Potion of Speed", 10),
            ("Spell Scroll, 6th Level", 10),
            ("Spell Scroll, 7th Level", 7),
            ("Ammunition, +3", 5),
            ("Oil of Sharpness", 5),
            ("Potion of Flying", 5),
            ("Potion of Cloud Giant Strength", 5),
            ("Potion of Longevity", 5),
            ("Potion of Vitality", 5),
            ("Spell Scroll, 8th Level", 5),
            ("Horseshoes of a Zephyr", 3),
            ("Nolzur's Marvelous Pigments", 3),
        ])
    elif rarity_type == "Minor" and rarity == "Legendary":
        table = OrderedDict([
            ("Spell Scroll, 8th Level", 30),
            ("Potion of Storm Giant Strength", 25),
            ("Potion of Supreme Healing", 15),
            ("Spell Scroll, 9th Level", 15),
            ("Universal Solvent", 8),
            ("Arrow of Slaying", 5),
            ("Sovereign Glue", 2),
        ])
    else:
        raise ValueError(rarity_type, rarity)

    for magic_item in load_magic_items().values():
        if magic_item["rarity_type"] == rarity_type and magic_item["rarity"] == rarity and \
                magic_item["name"] not in table.keys() and magic_item["name"] not in excluded_items:
            if "Dungeon" in magic_item["source"]:
                table[magic_item["name"]] = 1
    return table
