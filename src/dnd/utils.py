from enum import Enum

import toml
from typing import List, Optional, Union

from bottle import HTTPError, redirect, template
from src.common.utils import md_page, title_to_page_name

from os.path import join as pjoin, isfile
from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD


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
