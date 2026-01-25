import random
import re
import tomllib
from collections import defaultdict
from glob import glob
from os.path import join as pjoin, splitext, basename
from re import finditer
from typing import TypedDict, Literal, Any

from bottle import HTTPError, redirect, template
from bs4 import BeautifulSoup, NavigableString, Tag
from markdown2 import Markdown

from src.common.utils import title_to_page_name, str_to_list, md_page

NAMESPACE = "dnd"
INCLUDE_MD = """[[include dnd/monster-sheet.tpl]]
file = {}
[[/include]]"""


# Spells

SPELLS: dict[str, dict] = {}
SPELLS_BY_LEVEL: dict[int, list[dict]] = {}
ENUM_CACHE: dict[Literal["spell", "magic_item"], dict[str, set[str]]] = \
    {"spell": defaultdict(set), "magic_item": defaultdict(set)}
SORTED_ENUM_CACHE: dict[Literal["spell", "magic_item"], dict[str, list[str]]] = \
    {"spell": {}, "magic_item": {}}


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
            d["spell_lists_lower"] = [c.lower() for c in d["spell_lists"]]
            d["casting_time_md"] = MD.parse_md(d["casting_time"], namespace="dnd", with_metadata=False, no_p=True)
            d["range_md"] = MD.parse_md(d["range"], namespace="dnd", with_metadata=False, no_p=True)
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
            # Add values to enum cache
            add_to_enum_cache("spell", "casting_time", d["casting_time"])
            add_to_enum_cache("spell", "range", d["range"])
            add_to_enum_cache("spell", "duration", d["duration"])
            add_to_enum_cache("spell", "source", d["source"])
            spells[k] = d
            SPELLS_BY_LEVEL[int(d["level"])].append((k, d))
    except Exception as e:
        raise Exception(f"Error when trying to process {path}") from e
    print(" Done.", flush=True)
    sort_enum_cache()
    SPELLS = spells
    return SPELLS


def add_to_enum_cache(cache_type: Literal["spell", "magic_item"], key: str, value: Any):
    global ENUM_CACHE
    if key == "source":
        value = value.rsplit(",", 1)[0]
    if cache_type == "spell":
        if key == "casting_time":
            if value.startswith("Reaction"):
                value = "Reaction"
        elif key == "range":
            if value.startswith("Self"):
                value = "Self"
        elif key == "duration":
            if value.startswith("Concentration"):
                value = value.replace("Concentration, up to ", "")
            elif value.startswith("Up to"):
                value = value.replace("Up to ", "")
    elif cache_type == "magic_item":
        pass
    else:
        raise ValueError(f"Unknown cache_type {cache_type}")
    ENUM_CACHE[cache_type][key].add(value)


def sort_enum_cache():
    global SORTED_ENUM_CACHE
    for cache_type, caches in ENUM_CACHE.items():
        for key, values in caches.items():
            sort_dict = {}
            def sort_key(s: str):
                """
                Provides a sorting key that allows for increasing orders of duration, distance, etc to be sorted
                properly. E.g. 6 minutes, 10 minutes, 1 hour
                Create a `sort_dict` with the values to check for in the dict values
                """
                m = re.match(r"(\d+) (.*)", s)
                if not m:
                    return 99, 99, s
                for k, v in sort_dict.items():
                    if v in m.group(2):
                        return k, int(m.group(1)), s
                return 99, int(m.group(1)), s
            if key == "casting_time":
                sort_dict = {0: "bonus action", 1: "reaction", 2: "action", 3: "minute", 4: "hour"}
            elif key == "range":
                sort_dict = {0: "foot", 1: "feet", 2: "yard", 3: "mile"}
            elif key == "duration":
                sort_dict = {0: "round", 1: "minute", 2: "hour", 3: "day", 4: "week", 5: "month", 6: "year"}
            else:
                sort_key = None
            SORTED_ENUM_CACHE[cache_type][key] = sorted(values, key=sort_key)


def get_enum_cache(cache_type: Literal["spell", "magic_item"]) -> dict[str, list[str]]:
    load_magic_items()
    try:
        return SORTED_ENUM_CACHE[cache_type]
    except KeyError:
        raise ValueError(f"Unknown cache_type {cache_type}")


def get_magic_item_subtypes() -> list[str]:
    return get_enum_cache("magic_item")["subtype"]


def load_spells_by_level() -> dict[int, list[dict]]:
    load_spells()
    return SPELLS_BY_LEVEL


def class_spell(spell: dict, classes: list[str]) -> bool:
    """
    Helper function for determining if a spell belongs to any of a list of classes
    :param spell: The parsed spell dictionary, containing `spell_lists_lower` field, which has all the spell list
        names in lowercase
    :param classes: The list of classes to check against, all in lowercase.
    :return:
    """
    return bool(set(classes).intersection(spell["spell_lists_lower"]))


def filter_spells(filters: dict):
    results = {}
    results_by_level = defaultdict(list)
    spell_list_lower = [c.lower() for c in filters.get("spell_list", [])]
    for k, v in load_spells().items():
        if spell_list_lower:
            if not class_spell(v, spell_list_lower):
                continue
        if "level" in filters and v["level"].lower() not in filters["level"]:
            continue
        if "school" in filters and v["school"].lower() not in filters["school"]:
            continue
        if "casting_time" in filters:
            for t in filters["casting_time"]:
                if t.lower() in v["casting_time"].lower():
                    break
            else:
                continue
        if "range" in filters:
            for r in filters["range"]:
                if r.lower() in v["range"].lower():
                    break
            else:
                continue
        if "duration" in filters:
            for d in filters["duration"]:
                if d.lower() in v["duration"].lower():
                    break
            else:
                continue
        if "source" in filters:
            for s in filters["source"]:
                if s.lower() in v["source"].lower():
                    break
            else:
                continue
        if "concentration" in filters:
            if ((filters["concentration"] == "true" and not v["concentration_spell"]) or
                    (filters["concentration"] == "false" and v["concentration_spell"])):
                continue
        if "ritual" in filters:
            if ((filters["ritual"] == "true" and not v["ritual_spell"]) or
                    (filters["ritual"] == "false" and v["ritual_spell"])):
                continue
        if "verbal" in filters:
            if ((filters["verbal"] == "true" and "V" not in v["components"]) or
                    (filters["verbal"] == "false" and "V" in v["components"])):
                continue
        if "somatic" in filters:
            if ((filters["somatic"] == "true" and "S" not in v["components"]) or
                    (filters["somatic"] == "false" and "S" in v["components"])):
                continue
        if "material" in filters:
            if ((filters["material"] == "true" and "M" not in v["components"]) or
                    (filters["material"] == "false" and "M" in v["components"])):
                continue
        if "expensive" in filters:
            if ((filters["expensive"] == "true" and not v.get("expensive_material_component")) or
                    (filters["expensive"] == "false" and v.get("expensive_material_component"))):
                continue
        if "consumed" in filters:
            if ((filters["consumed"] == "true" and not v.get("material_component_consumed")) or
                    (filters["consumed"] == "false" and v.get("material_component_consumed"))):
                continue
        results[k] = v
        results_by_level[v["level"]].append((k, v))
    return results, results_by_level


# Magic Items

MAGIC_ITEMS = None

def load_magic_items():
    global MAGIC_ITEMS
    if MAGIC_ITEMS:
        return MAGIC_ITEMS
    magic_items = {}
    path = None
    print("Loading magic items into memory", end='')
    from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
    try:
        for path in sorted(glob(f"data/{NAMESPACE}/equipment/magic-items/*")):
            print(".", end='', flush=True)
            with open(path) as f:
                d = tomllib.loads(f.read())
            # Do some special handling
            d["description"] = d["description"].strip()
            d["description_md"] = MD.parse_md(d["description"], namespace=NAMESPACE, with_metadata=False)
            # Add values to enum cache
            add_to_enum_cache("magic_item", "source", d["source"])
            if d["subtype"]:
                add_to_enum_cache("magic_item", "subtype", d["subtype"])
            # Write to dict
            magic_items[splitext(basename(path))[0]] = d
    except Exception:
        print(f"\nError when trying to process {path}")
        raise
    print(" Done.", flush=True)
    sort_enum_cache()
    MAGIC_ITEMS = magic_items
    return MAGIC_ITEMS


def filter_magic_items(filters) -> dict[str, dict]:
    d = {}
    magic_items = load_magic_items()
    for k, v in magic_items.items():
        if v.get("unlisted"):
            continue
        table_name = filters.get("table_name")
        if table_name and table_name != "any" and table_name not in v["tables"]:
            continue
        if "type" in filters and v["type"] not in filters["type"]:
            continue
        if "rarity" in filters and v["rarity"] not in filters["rarity"]:
            continue
        if "attunement" in filters:
            if (filters["attunement"] == "true" and not v["attunement"] or
                    filters["attunement"] == "false" and v["attunement"]):
                continue
        if "subtype" in filters:
            if v["subtype"]:
                if v["subtype"] not in filters["subtype"]:
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


def generate_magic_items(filter_keys: dict, max_items: int, no_duplicates: bool) -> list[tuple[str, str]]:
    magic_items = filter_magic_items(filter_keys)
    magic_item_keys = list(magic_items.keys())
    spells_by_level = load_spells_by_level()
    generated_magic_items = []
    for _ in range(max_items):
        magic_item_key = random.choice(magic_item_keys)
        magic_item = magic_items[magic_item_key]
        generated_magic_item = [magic_item["name"], None]
        # Add random spell to the end of the item name if necessary
        m = re.search(r"(?:spell-scroll-|enspelled-[a-z]+-)(.+)$", magic_item_key)
        if m:
            if m.group(1) == "cantrip":
                level = 0
            else:
                # E.g. "level-1" -> 1
                level = int(m.group(1).split("-")[1])
            _, random_spell = random.choice(spells_by_level[level])
            generated_magic_item[1] = random_spell["title"]
        else:
            # If it's not a spell scroll, and we want to avoid duplicates, remove the chosen item from set
            if no_duplicates:
                magic_item_keys.remove(magic_item_key)
                if len(magic_item_keys) == 0:
                    break
        generated_magic_items.append(tuple(generated_magic_item))
    return generated_magic_items


# Tooltips

class TooltipEntry(TypedDict):
    href: str
    content: str | list[str]

TooltipDict = dict[str, TooltipEntry]
TOOLTIP_MAX_LENGTH = 1000


def split_rules_glossary() -> TooltipDict:
    md = Markdown()
    with open("data/dnd/general/rules-glossary.md") as f:
        page = f.read()
    rules_glossary = {}
    page = clean_custom_markdown(page)
    split_page = re.split(r"^## ", page, flags=re.MULTILINE)
    for text in split_page[1:]:
        if not text:
            continue
        name, content = text.split("\n", maxsplit=1)
        href = title_to_page_name(name)
        m = re.match(r"^(.*) \[.*]$", name.lower())
        if m:
            name = m.group(1)
        # print(f"Truncating {name}")
        content = truncate_html_by_visible_text(content)
        rules_glossary[name.lower()] = {
            "href": "/dnd/general/Rules Glossary#" + href,
            "content": md.convert(content).strip(" \n"),
        }
    return rules_glossary


def split_equipment() -> TooltipDict:
    md = Markdown()
    with open("data/dnd/general/equipment.md") as f:
        page = f.read()
    tooltips = {}
    save_text = False
    table_type = None
    key = ""
    page = clean_custom_markdown(page)
    for line in page.split("\n"):
        if not line:
            continue
        if line.startswith("# ") or line.startswith("## "):
            if line in ("## Properties", "## Mastery Properties", "## Artisan's Tools", "## Other Tools", "## Adventuring Gear"):
                save_text = True
                table_type = "Misc"
            elif line == "## Weapons":
                save_text = True
                table_type = "Weapons"
            elif line == "## Armor Tables":
                save_text = True
                table_type = "Armor"
            else:
                save_text = False
            key = ""
            continue
        if save_text:
            if table_type in ("Weapons", "Armor"):
                key, d = make_tooltip_from_table(line, table_type)
                if key:
                    tooltips[key] = d
            else:
                if line.startswith("### "):
                    key = line.strip("#").strip().lower()
                    href = title_to_page_name(key)
                    tooltips[key] = {
                        "href": "/dnd/general/Equipment#" + href,
                        "content": [],
                    }
                elif key:
                    if line.startswith("#### "):
                        # Don't include header lines or anything following them in the tooltips
                        key = ""
                    else:
                        tooltips[key]["content"].append(line)

    for key, d in tooltips.items():
        content = "\n\n".join(d["content"])
        content = md.convert(content).strip(" \n")
        # print(f"Truncating {key}")
        content = truncate_html_by_visible_text(content)
        d["content"] = content

    return tooltips


def clean_custom_markdown(text: str) -> str:
    """Remove custom markdown (i.e. things in [[]] or [[[]]]) before parsing. Replace with italics."""
    for m in finditer(r"_?\[?\[\[.*?:(.*?)(\|(.*?))?]]]?_?", text):
        text = text.replace(m.group(0), f"_{m.group(3) or m.group(1)}_")
    return text


def make_tooltip_from_table(line: str, table_type: str) -> tuple[str, TooltipEntry | None]:
    if line.startswith("|"):
        cells = str_to_list(line, delimiter="|")
        key = cells[0].strip("_").lower()
        if key == "name" or key.startswith("---"):
            return "", None

        if table_type == "Weapons":
            content = f"**Damage:** {cells[1]}  **Mastery:** {cells[3]}  \n**Weight:** {cells[4]}  **Cost:** {cells[5]}  \n**Properties:** {cells[2]}"
            href = "/dnd/general/Equipment#weapons"
        elif table_type == "Armor":
            content = f"**AC:** {cells[1]}  \n**Weight:** {cells[4]}  **Cost:** {cells[5]}"
            if cells[2] != "--":
                content += f"  \n**Strength Required:** {cells[2]}"
            if cells[3] != "--":
                content += f"  \nDisadvantage on Stealth"
            href = "/dnd/general/Equipment#armor"
        else:
            raise ValueError(f"How the fuck did this happen? {table_type}")

        d: TooltipEntry = {
            "href": "/dnd/general/Equipment#" + href,
            "content": [content],
        }
        return key, d
    return "", None


def truncate_html_by_visible_text(html: str) -> str:
    """
    Truncate HTML string by visible text length, ensuring no HTML tags are broken.
    Appends ' ... <em>[more]</em>' if truncated.
    """
    def truncate_elements(e: Tag | NavigableString, delete_current_element: bool = False):
        """
        Truncate all elements after the current one, in the current element's parent and all parents above.
        This will guarantee that the visible text ends at the truncated text.
        """
        offset = 0 if delete_current_element else 1
        current = e
        while current.parent is not None:
            parent = current.parent
            index = parent.contents.index(current)
            del parent.contents[index + offset:]
            # Don't delete current element for any parents
            offset = 1
            current = parent

    soup = BeautifulSoup(html, 'html.parser')
    visible_text = soup.get_text()
    if len(visible_text) <= TOOLTIP_MAX_LENGTH:
        return html
    current_length = 0
    for element in soup.descendants:
        # Stop early if we get to table headers. We don't want to include tables in the tooltips.
        if isinstance(element, Tag) and 'table-header' in element.get('class', []):
            truncate_elements(element, delete_current_element=True)
            return str(soup)
        if isinstance(element, NavigableString):
            text = element.string
            if current_length + len(text) <= TOOLTIP_MAX_LENGTH:
                current_length += len(text)
            else:
                # Delete all elements after this one
                truncate_elements(element)
                # Replace the text in the current element so we don't exceed the max length
                excess = (current_length + len(text)) - TOOLTIP_MAX_LENGTH
                truncated_text = text[:-excess]
                element.replace_with(NavigableString(truncated_text))
                break
    else:
        raise ValueError("How did you get here?")

    # Test that visible text is under limit before appending more
    visible_after = soup.get_text()
    if not len(visible_after) <= TOOLTIP_MAX_LENGTH:
        raise AssertionError(f"Truncation failed: {len(visible_after)} > {TOOLTIP_MAX_LENGTH}")

    soup.append(NavigableString(' ... '))
    more_tag = soup.new_tag('em')
    more_tag.string = '[more]'
    soup.append(more_tag)

    return str(soup)


def open_monster_sheet(name: str):
    try:
        return md_page(name, NAMESPACE, "monster", build_toc=False)
    except HTTPError as e:
        if e.status_code != 404:
            raise
        # If we can't find a template or MD file, check for a TOML file itself and just load the monster-sheet
        toml_path = pjoin(NAMESPACE, "monster", title_to_page_name(name) + ".toml")
        try:
            with open(pjoin("data", toml_path)) as f:
                toml_dict = tomllib.loads(f.read())
        except FileNotFoundError:
            raise HTTPError(404, f"Can't find a page for \"/{NAMESPACE}/monster/{name}\"")
        if "redirect" in toml_dict:
            return redirect(toml_dict["redirect"])
        # Avoiding circular dependencies
        from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER as MD
        md_text = MD.parse_md(INCLUDE_MD.format(toml_path), namespace=NAMESPACE)
        return template("common/page.tpl", {"title": toml_dict["name"], "text": md_text})
