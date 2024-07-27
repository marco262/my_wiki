from collections import OrderedDict, defaultdict
from enum import Enum
from glob import glob
from os.path import join as pjoin, isfile, splitext, basename
from typing import List, Optional, Union

import toml
from bottle import HTTPError, redirect, template

from src.common.utils import md_page, title_to_page_name


class Mode(Enum):
    TITLE = "TITLE"
    BRIEF = "BRIEF"
    FULL = "FULL"


INCLUDE_MD = """[[include dnd/monster-sheet.tpl]]
file = {}
[[/include]]"""
SPELLS = None
SPELLS_BY_LEVEL = None
MAGIC_ITEMS = None
MAGIC_ITEM_SUBTYPES = []


def init_spells_and_magic_items():
    global SPELLS, MAGIC_ITEMS
    SPELLS = {}
    MAGIC_ITEMS = {}


def class_spell(spell: dict, classes: List[str], ua_spells: bool) -> bool:
    """
    Helper function for determining if a spell belongs to any of a list of classes
    :param spell: The parsed spell dictionary, containing classes and classes_ua fields
    :param classes: The list of classes to check against
    :param ua_spells: Whether to include the classes_ua field in the spell
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
        # Avoiding circular dependencies
        from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
        md_text = MD.parse_md(INCLUDE_MD.format(toml_path), namespace="dnd")
        return template("common/page.tpl", {"title": toml_dict["name"], "text": md_text})


def load_spells():
    global SPELLS, SPELLS_BY_LEVEL
    if SPELLS:
        return SPELLS
    spell_by_level = defaultdict(list)
    spells = {}
    path = None
    print("Loading spells into memory", end='')
    from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
    try:
        for path in sorted(glob("data/dnd/spell/*")):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd", with_metadata=False)
            if "source_extended" in d:
                d["source_extended"] = MD.parse_md(d["source_extended"], namespace="dnd", with_metadata=False)
            k = splitext(basename(path))[0]
            spells[k] = d
            spell_by_level[d["level"]].append((k, d))
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    SPELLS, SPELLS_BY_LEVEL = spells, spell_by_level
    return SPELLS


def load_spells_by_level():
    load_spells()
    return SPELLS_BY_LEVEL


def filter_spells(filters: dict):
    results = defaultdict(list)
    for k, v in load_spells().items():
        if "class" in filters:
            if not class_spell(v, filters["class"], filters.get("ua_spells", True)):
                continue
        if "level" in filters and v["level"] not in filters["level"]:
            continue
        if "school" in filters and v["school"] not in filters["school"]:
            continue
        if "casting_time" in filters:
            for t in filters["casting_time"]:
                if t in v["casting_time"]:
                    break
            else:
                continue
        if "range" in filters:
            for t in filters["range"]:
                if t in v["range"]:
                    break
            else:
                continue
        if "duration" in filters:
            for d in filters["duration"]:
                if d in v["duration"]:
                    break
            else:
                continue
        if "source" in filters:
            for s in filters["source"]:
                if s in v["source"]:
                    break
            else:
                continue
        if "concentration" in filters:
            if ((filters["concentration"] == "yes" and not v["concentration_spell"]) or
                    (filters["concentration"] == "no" and v["concentration_spell"])):
                continue
        if "ritual" in filters:
            if ((filters["ritual"] == "yes" and not v["ritual_spell"]) or
                    (filters["ritual"] == "no" and v["ritual_spell"])):
                continue
        if "verbal" in filters:
            if ((filters["verbal"] == "yes" and "V" not in v["components"]) or
                    (filters["verbal"] == "no" and "V" in v["components"])):
                continue
        if "somatic" in filters:
            if ((filters["somatic"] == "yes" and "S" not in v["components"]) or
                    (filters["somatic"] == "no" and "S" in v["components"])):
                continue
        if "material" in filters:
            if ((filters["material"] == "yes" and "M" not in v["components"]) or
                    (filters["material"] == "no" and "M" in v["components"])):
                continue
        if "expensive" in filters:
            if ((filters["expensive"] == "yes" and not v.get("expensive_material_component")) or
                    (filters["expensive"] == "no" and v.get("expensive_material_component"))):
                continue
        if "consumed" in filters:
            if ((filters["consumed"] == "yes" and not v.get("material_component_consumed")) or
                    (filters["consumed"] == "no" and v.get("material_component_consumed"))):
                continue
        results[v["level"]].append((k, v))
    return results


def load_magic_items():
    global MAGIC_ITEMS, MAGIC_ITEM_SUBTYPES
    if MAGIC_ITEMS:
        return MAGIC_ITEMS
    MAGIC_ITEM_SUBTYPES = set()
    magic_items = {}
    path = None
    print("Loading magic items into memory", end='')
    from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
    try:
        for path in sorted(glob("data/dnd/equipment/magic-items/*")):
            print(".", end='', flush=True)
            with open(path) as f:
                d = toml.loads(f.read(), _dict=OrderedDict)
            d["description"] = d["description"].strip()
            d["description_md"] = MD.parse_md(d["description"], namespace="dnd", with_metadata=False)
            if d["subtype"]:
                MAGIC_ITEM_SUBTYPES.add(d["subtype"])
            magic_items[splitext(basename(path))[0]] = d
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    MAGIC_ITEMS = magic_items
    MAGIC_ITEM_SUBTYPES = sorted(MAGIC_ITEM_SUBTYPES)
    return MAGIC_ITEMS


def get_magic_item_subtypes():
    load_magic_items()
    return MAGIC_ITEM_SUBTYPES


def filter_magic_items(filters):
    d = {}
    for k, v in load_magic_items().items():
        if v.get("unlisted"):
            continue
        if "type" in filters and v["type"].lower() not in filters["type"]:
            continue
        if "rarity" in filters and v["rarity"].lower() not in filters["rarity"]:
            continue
        if "major-minor" in filters and v["rarity_type"].lower() not in filters["minor-major"]:
            continue
        if "attunement" in filters:
            if (filters["attunement"] == "true" and not v["attunement"] or
                    filters["attunement"] == "false" and v["attunement"]):
                continue
        if "subtype" in filters:
            if v["subtype"]:
                if v["subtype"].lower() not in filters["subtype"]:
                    continue
            else:
                if "no-subtype" not in filters["subtype"]:
                    continue
        if "classes" in filters:
            if v["classes"]:
                if not set(v["classes"]).intersection(filters["classes"]):
                    continue
            else:
                if "no-restrictions" not in filters["classes"]:
                    continue
        if "source" in filters:
            for s in filters["source"]:
                if s.lower() in v["source"].lower():
                    break
            else:
                continue
        d[k] = v
    return d


def get_magic_item_table(filtered_magic_items, rarity_type, rarity):
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
        excluded_items = ["Arrow of Slaying"]
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
    elif rarity_type == "Major" and rarity == "Uncommon":
        table = OrderedDict([
            ("Weapon, +1", 15),
            ("Shield, +1", 3),
            ("Sentinel Shield", 3),
            ("Amulet of Proof Against Detection and Location", 2),
            ("Boots of Elvenkind", 2),
            ("Boots of Striding and Springing", 2),
            ("Bracers of Archery", 2),
            ("Brooch of Shielding", 2),
            ("Broom of Flying", 2),
            ("Cloak of Elvenkind", 2),
            ("Cloak of Protection", 2),
            ("Gauntlets of Ogre Power", 2),
            ("Hat of Disguise", 2),
            ("Javelin of Lightning", 2),
            ("Pearl of Power", 2),
            ("Rod of the Pact Keeper, +1", 2),
            ("Slippers of Spider Climbing", 2),
            ("Staff of the Adder", 2),
            ("Staff of the Python", 2),
            ("Sword of Vengeance", 2),
            ("Trident of Fish Command", 2),
            ("Wand of Magic Missiles", 2),
            ("Wand of the War Mage, +1", 2),
            ("Wand of Web", 2),
            ("Weapon of Warning", 2),
            ("Adamantine Armor (chain mail)", 1),
            ("Adamantine Armor (chain shirt)", 1),
            ("Adamantine Armor (scale mail)", 1),
            ("Bag of Tricks (gray)", 1),
            ("Bag of Tricks (rust)", 1),
            ("Bag of Tricks (tan)", 1),
        ])
        excluded_items = ["Adamantine Armor", "Bag of Tricks"]
    elif rarity_type == "Major" and rarity == "Rare":
        table = OrderedDict([
            ("Weapon, +2", 11),
            ("Adamantine Armor (breastplate)", 1),
            ("Adamantine Armor (splint)", 1),
            ("Armor, +1 (leather)", 1),
            ("Armor, +1 (chain shirt)", 1),
            ("Armor, +1 (chain mail)", 1),
            ("Armor, +1 (scale mail)", 1),
            ("Armor of Resistance (leather)", 1),
            ("Armor of Resistance (chain shirt)", 1),
            ("Armor of Resistance (chain mail)", 1),
            ("Armor of Resistance (scale mail)", 1),
        ])
        excluded_items = ["Armor, +1", "Armor of Resistance"]
    elif rarity_type == "Major" and rarity == "Very Rare":
        table = OrderedDict([
            ("Weapon, +3", 10),
            ("Amulet of the Planes", 2),
            ("Carpet of Flying", 2),
            ("Crystal Ball", 2),
            ("Ring of Regeneration", 2),
            ("Ring of Shooting Stars", 2),
            ("Ring of Telekinesis", 2),
            ("Robe of Scintillating Colors", 2),
            ("Robe of Stars", 2),
            ("Rod of Absorption", 2),
            ("Rod of Alertness", 2),
            ("Rod of Security", 2),
            ("Rod of the Pact Keeper, +3", 2),
            ("Scimitar of Speed", 2),
            ("Shield, +3", 2),
            ("Staff of Fire", 2),
            ("Staff of Frost", 2),
            ("Staff of Power", 2),
            ("Staff of Striking", 2),
            ("Staff of Thunder and Lightning", 2),
            ("Sword of Sharpness", 2),
            ("Wand of Polymorph", 2),
            ("Wand of the War Mage, +3", 2),
            ("Adamantine Armor (half plate)", 1),
            ("Adamantine Armor (plate)", 1),
            ("Armor, +1 (studded leather)", 1),
            ("Armor, +1 (breastplate)", 1),
            ("Armor, +1 (splint)", 1),
            ("Armor of Resistance (studded leather)", 1),
            ("Armor of Resistance (breastplate)", 1),
            ("Armor of Resistance (splint)", 1),
            ("Armor, +2 (leather)", 1),
            ("Armor, +2 (chain shirt)", 1),
            ("Armor, +2 (chain mail)", 1),
            ("Armor, +2 (scale mail)", 1),
        ])
        excluded_items = ["Armor, +2"]
    elif rarity_type == "Major" and rarity == "Legendary":
        table = OrderedDict([
            ("Defender", 5),
            ("Hammer of Thunderbolts", 5),
            ("Luck Blade", 5),
            ("Sword of Answering", 5),
            ("Holy Avenger", 3),
            ("Ring of Djinni Summoning", 3),
            ("Ring of Invisibility", 3),
            ("Ring of Spell Turning", 3),
            ("Rod of Lordly Might", 3),
            ("Staff of the Magi", 3),
            ("Vorpal Sword", 3),
            ("Belt of Cloud Giant Strength", 2),
            ("Armor, +2 (breastplate)", 2),
            ("Armor, +3 (chain mail)", 2),
            ("Armor, +3 (chain shirt)", 2),
            ("Cloak of Invisibility", 2),
            ("Armor, +1 (half plate)", 2),
            ("Iron Flask", 2),
            ("Armor, +3 (leather)", 2),
            ("Armor, +1 (plate)", 2),
            ("Robe of the Archmagi", 2),
            ("Rod of Resurrection", 2),
            ("Armor, +1 (scale mail)", 2),
            ("Scarab of Protection", 2),
            ("Armor, +2 (splint)", 2),
            ("Armor, +2 (studded leather)", 2),
            ("Well of Many Worlds", 2),
            ("Armor, +2 (half plate)", 2),
            ("Armor, +2 (plate)", 2),
            ("Armor, +3 (studded leather)", 2),
            ("Armor, +3 (breastplate)", 2),
            ("Armor, +3 (splint)", 2),
            ("Armor, +3 (half plate)", 1),
            ("Armor, +3 (plate)", 1),
            ("Armor of Resistance (half plate)", 1),
            ("Armor of Resistance (plate)", 1),
        ])
        excluded_items = ["Armor, +3"]
    else:
        raise ValueError(rarity_type, rarity)

    # Remove items that are not already in the included list of filtered magic items
    for k, v in list(table.items()):
        if k not in filtered_magic_items:
            del table[k]

    # Add more items to the table that fit the rarity_type and rarity
    for magic_item in filtered_magic_items.values():
        if magic_item["rarity_type"] == rarity_type and magic_item["rarity"] == rarity and \
                magic_item["name"] not in table.keys() and magic_item["name"] not in excluded_items:
            table[magic_item["name"]] = 1
    return table
