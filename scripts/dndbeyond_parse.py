"""
Copy the HTML content from D&D Beyond into a file (no nav bar, no header, etc.), and put that file's path in PATH.
This script will then convert that file into a Markdown representation of that file.
It will also add a "Source:" section at the end. Make sure to fill that out manually using a real book reference
like "Player's Handbook, p. 34".
"""
import re
import os

import bs4
from bs4 import Tag, NavigableString

from data.dnd.enums import custom_tooltips
from src.dnd.utils import split_rules_glossary, split_equipment

PATH = "data/dnd/dm/treasure.md"


os.chdir("..")
GLOSSARY_TOOLTIPS = split_rules_glossary()
EQUIPMENT_TOOLTIPS = split_equipment()


def main() -> None:
    # Load the HTML file into Beautiful Soup
    with open(PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace "smart" quotes
    html_content = html_content.replace("’", "'")
    html_content = html_content.replace("&rsquo;", "'")
    html_content = html_content.replace("“", '"')
    html_content = html_content.replace("”", '"')
    html_content = html_content.replace("—", " -- ")

    soup = bs4.BeautifulSoup(html_content, "html.parser")

    output = []
    for tag in soup:  # type: Tag
        if isinstance(tag, NavigableString):
            continue
        output.append(parse_tag(tag))
    output = "\n\n".join(output)

    if not output:
        print(f"No HTML found in {PATH}")
        return

    output += """
----

_Source: Dungeon Master's Guide, p. XXX_
"""

    print(output)

    with open(PATH, "w", encoding="utf-8") as file:
        file.write(output)


def parse_tag(parent: Tag) -> str:
    if isinstance(parent, NavigableString):
        return ""
    # print(parent)
    # Match on top-level elements
    match parent.name:
        case "table":
            return parse_table(parent)
        case "ul":
            return parse_ul(parent)
        case "hr":
            return "---"
        case str() as s if s.startswith("h"):
            return parse_header(parent)
        case "caption":
            tag = parent.find()
            if tag:
                return parse_tag(tag)
        case "div":
            return parse_div(parent)
        case "aside":
            return parse_aside(parent)

    output = []
    for tag in parent:  # type: Tag
        match tag.name:
            case None:
                text = tag.get_text()
                if text and text != "\n":
                    output.append(text)
            case "p":
                output.append(parse_tag(tag))
            case "strong":
                output.append(f"**{parse_tag(tag)}**")
            case "em":
                output.append(f"_{parse_tag(tag)}_")
            case "a":
                output.append(parse_link(tag, parent.name))
            case "table":
                output.append(parse_table(tag))
            case "div":
                output.append(parse_div(tag))
            case "br":
                output.append("\n")
            case "span":
                output.append(tag.text)
            case "figcaption":
                pass
            case _:
                raise ValueError(f"Unhandled tag: {tag}")

    return "".join(output)


def parse_header(header: Tag) -> str:
    prefix = ""
    match header.name:
        case "h2":
            prefix = "# "
        case "h3":
            prefix = "## "
        case "h4":
            prefix = "### "
        case "h5":
            prefix = "#### "
        case _:
            raise ValueError(header.name)
    # Condense multiple spaces into single spaces
    text = " ".join(header.get_text().split())
    return prefix + text


def parse_table(table: Tag) -> str:
    # If no header in this table, assume it's a weird table we want to make into a bulleted list
    output = []
    for tag in table:  # type: Tag
        match tag.name:
            case "caption":
                output.append(parse_tag(tag))
                output.append("")
            case "thead":
                for row in tag:  # type: Tag
                    output += parse_row(row, header=True)
            case "tbody":
                for row in tag:  # type: Tag
                    output += parse_row(row)
    return "\n".join(output)


def parse_row(row: Tag, header: bool = False) -> list[str]:
    if isinstance(row, NavigableString):
        return []
    cell_text_list = []
    for cell in row:  # type: Tag
        cell_text = parse_tag(cell)
        if not cell_text:
            continue
        cell_text_list.append(cell_text)
    output = [markdown_row(cell_text_list)]
    if header:
        output.append(markdown_header_sep(len(cell_text_list)))
    return output


def parse_table_raw(table: Tag) -> str:
    # If no header in this table, assume it's a weird table we want to make into a bulleted list
    output = ["<table>"]
    for tag in table:  # type: Tag
        match tag.name:
            case "caption":
                output.append(parse_tag(tag))
                output.append("")
            case "thead":
                output.append("<thead>")
                for row in tag:  # type: Tag
                    output += parse_row_raw(row, header=True)
                output.append("</thead>")
            case "tbody":
                output.append("<tbody>")
                for row in tag:  # type: Tag
                    output += parse_row_raw(row)
                output.append("</tbody>")
    output.append("</table>")
    return "\n".join(output)


def parse_row_raw(row: Tag, header: bool = False) -> list[str]:
    if isinstance(row, NavigableString):
        return []
    tag = "th" if header else "td"
    output = ["  <tr>"]
    for cell in row:  # type: Tag
        cell_text = parse_tag(cell)
        if not cell_text:
            continue
        output.append(f"    <{tag}>{cell_text}</{tag}>")
    output.append("  </tr>")
    return output


def markdown_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def markdown_header_sep(num_cells: int) -> str:
    return "|" + "|".join(["---"] * num_cells) + "|"


def parse_link(tag: Tag, parent_name: str) -> str:
    text = tag.get_text()
    if "class" not in tag.attrs:
        href = tag.attrs['href']
        split_href = href.split("#", 1)
        href = split_href[0]
        if len(split_href) == 2:
            anchor = parse_anchor(split_href[1])
        else:
            anchor = ""

        # Handle internal links special, so I can link to other places on my wiki
        my_wiki_path = ""
        match href:
            case "/sources/dnd/phb-2024/creating-a-character":
                my_wiki_path = "advancement:Creating a Character"
            case "/sources/dnd/phb-2024/equipment":
                my_wiki_path = "general:Equipment"
            case "/sources/dnd/dmg-2024/creating-adventures":
                my_wiki_path = "dm:Creating Adventures"
            case "/sources/dnd/dmg-2024/dms-toolbox":
                my_wiki_path = "dm:DM's Toolbox"
            case "/sources/dnd/dmg-2024/random-magic-items":
                my_wiki_path = "dm:Random Magic Items"
            case _:
                if "sources" in href:
                    raise ValueError(href)
        if my_wiki_path:
            link_in_table = parent_name in ("td", "th")
            if anchor:
                my_wiki_path += "#" + anchor
            include_text = not my_wiki_path.lower().endswith(text.lower())
            if include_text:
                if link_in_table:
                    # Avoid using my internal linking format so we don't mess up the table
                    my_wiki_path = my_wiki_path.replace(":", "/")
                    return f"[{text}](/dnd/{my_wiki_path})"
                else:
                    return f"[[[{my_wiki_path}|{text}]]]"
            else:
                return f"[[[{my_wiki_path}]]]"

        # Generic link
        if anchor:
            if text == anchor:
                return f"[{text}](#)"
            return f"[{text}]({href}#{anchor})"
        return f"[{text}]({href})"


    classes = tag.attrs["class"]
    if ("ddb-lightbox-inner" in classes) or ("ddb-lightbox-outer" in classes):
        return ""
    if "spell-tooltip" in classes:
        return f"[[[spell:{text}]]]"
    if "monster-tooltip" in classes:
        return f"[[[monster:{text}]]]"
    if "sourcebook" in classes:
        return f"_{text}_"

    if "magic-item-tooltip" in classes:
        return f"[[tooltip:{text}]]"

    tooltip_classes = ["skill-tooltip"]
    for c in tooltip_classes:
        if c in classes:
            return make_tooltip("tooltip", custom_tooltips, text)

    glossary_classes = ["condition-tooltip", "action-tooltip", "rule-tooltip", "sense-tooltip"]
    for c in glossary_classes:
        if c in classes:
            return make_tooltip("glossary", GLOSSARY_TOOLTIPS, text)

    equipment_classes = ["item-tooltip", "weapon-properties-tooltip"]
    for c in equipment_classes:
        if c in classes:
            return make_tooltip("tooltip", EQUIPMENT_TOOLTIPS, text)

    # Unhandled
    equipment_classes = ["lore-tooltip"]
    for c in equipment_classes:
        if c in classes:
            return f"[[tooltip:{text}]]"

    raise ValueError(f"Unhandled link: {tag}")


def parse_anchor(text: str) -> str:
    for n in re.finditer(r"([A-Z])", text):
        text = text.replace(n.group(1), " " + n.group(1))
    text = text.replace("of", " of")
    text = text.replace("the", " the")
    text = text.replace("and", " and")
    text = text.replace("from", " from")
    # Remove accidental double spaces
    text = re.sub("\s\s+", " ", text)
    return text.strip(" ")


def make_tooltip(tooltip_type: str, tooltip_dict: dict, text: str) -> str:
    key = text.lower()
    if key in tooltip_dict:
        return f"[[{tooltip_type}:{text}]]"
    else:
        k = key.rstrip("s")
        if k in tooltip_dict:
            return f"[[{tooltip_type}:{k}|{text}]]"

        k = key.rstrip("es")
        if k in tooltip_dict:
            return f"[[{tooltip_type}:{k}|{text}]]"

        match text:
            case "Half Cover":
                return f"[[tooltip:Half Cover]]"
            case "Three-Quarters Cover":
                return f"[[tooltip:Three-Quarters Cover]]"
            case "Total Cover":
                return f"[[tooltip:Total Cover]]"
            case str() as s if (m := re.match(r"Arcane Focus \((.*?)\)", s)):
                return f"[[tooltip:Arcane Focus]] ({m.group(1)})"
            case "Short":
                # Assume it means Short Rest
                return f"[[glossary:Short Rest|Short]]"
            case "Long":
                # Assume it means Long Jump (double-check this)
                return f"[[glossary:Long Jump|Long]]"
            case "shape-shift":
                # Assume it means Shifting
                return f"[[glossary:Shifting|shape-shift]]"
            case "Opportunity Attack":
                # Assume it means Opportunity Attacks
                return f"[[glossary:Opportunity Attacks|Opportunity Attack]]"
        raise ValueError(f"Undefined tooltip: {text}")


def parse_ul(parent: Tag) -> str:
    output = []
    for tag in parent:  # type: Tag
        if isinstance(tag, NavigableString):
            continue
        output.append(" - " + parse_tag(tag))
    return "\n".join(output)


def parse_div(parent: Tag) -> str:
    output = []
    sep = "\n"

    if "class" in parent.attrs:
        classes = parent.attrs["class"]

        # Parse divs that should return raw text
        text_classes = ["stat-block"]
        for c in text_classes:
            if c in classes:
                return parent.text

        # Parse divs that contain uls
        ul_classes = ["effect-info", "effects-info", "spell-components", "flexible-quad-column", "condensed-group", "hangingIndent"]
        for c in ul_classes:
            if c in classes:
                return parse_ul(parent)

        # Parse divs with multiple parseable tags within
        ignorable_classes = [
            "subitems-list-details",
            "flexible-double-column",
            "flexible-double-column__column-width-20pct",
            "flexible-double-column__column-width-30pct",
            "flexible-double-column__column-width-40pct",
            "ui-droppable",
            "compendium--center",
        ]
        handled_classes = [
            "subitems-list-details-item",
            "p-article-content",
        ]
        for c in ignorable_classes:
            if c in classes:
                sep = ""
                break
        else:
            for c in handled_classes:
                if c in classes:
                    break
            else:
                raise ValueError(f"Unhandled div: {classes}")

    for tag in parent:  # type: Tag
        output.append(parse_tag(tag))
    return sep.join(output)


def parse_aside(parent: Tag) -> str:
    output = ["[[sidebar]]"]
    for tag in parent:  # type: Tag
        output.append(parse_tag(tag))
    output.append("[[/sidebar]]")
    return "\n".join(output)


if __name__ == "__main__":
    main()
    # a = """<a class="tooltip-hover skill-tooltip" data-tooltip-href="/skills/11-tooltip" href="/sources/dnd/free-rules/playing-the-game#Skills">Animal Handling</a>"""
    # b = bs4.BeautifulSoup(a, "html.parser")
    # print(parse_link(b.find()))
