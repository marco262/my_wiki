"""
Copy the HTML content from D&D Beyond into a file (no nav bar, no header, etc.), and put that file's path in PATH.
This script will then convert that file into a Markdown representation of that file.
It will also add a "Source:" section at the end. Make sure to fill that out manually using a real book reference
like "Player's Handbook, p. 34".
"""
import os

import bs4
from bs4 import Tag, NavigableString

from data.dnd.enums import tooltips
from src.dnd.utils import split_rules_glossary

os.chdir("..")
PATH = "data/dnd/class/monk.md"
GLOSSARY_TOOLTIPS = split_rules_glossary()


def main() -> None:
    # Load the HTML file into Beautiful Soup
    with open(PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace "smart" quotes
    html_content = html_content.replace("’", "'")
    html_content = html_content.replace("&rsquo;", "'")

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

_Source: Player's Handbook, p. XXX_
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
        case str() as s if s.startswith("h"):
            return parse_header(parent)
        case "caption":
            tag = parent.find()
            if tag:
                return parse_tag(tag)
        case "div":
            return parse_div(parent)

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
                output.append(parse_link(tag))
            case "table":
                return parse_table(tag)
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
    has_header = bool(table.find("thead"))
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
                if has_header:
                    for row in tag:  # type: Tag
                        output += parse_row(row)
                else:
                    for row in tag:
                        output += parse_headless_row(row)
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


def parse_headless_row(row: Tag) -> list[str]:
    if isinstance(row, NavigableString):
        return []
    output = []
    for cell in row:  # type: Tag
        cell_text = parse_tag(cell)
        match cell.name:
            case "th":
                output.append(f" - **{cell_text}**:")
            case "td":
                output.append(cell_text)
    return [" ".join(output)]


def markdown_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def markdown_header_sep(num_cells: int) -> str:
    return "|" + "|".join(["---"] * num_cells) + "|"


def parse_link(tag: Tag) -> str:
    text = tag.get_text()
    if "class" not in tag.attrs:
        return f"[{text}]({tag.attrs['href']})"

    classes = tag.attrs["class"]
    if "spell-tooltip" in classes:
        return f"_[[[spell:{text}]]]_"
    tooltip_classes = ["skill-tooltip", "item-tooltip", "weapon-properties-tooltip"]
    for c in tooltip_classes:
        if c in classes:
            return make_tooltip("tooltip", tooltips, text)

    glossary_classes = ["condition-tooltip", "action-tooltip", "rule-tooltip", "sense-tooltip"]
    for c in glossary_classes:
        if c in classes:
            return make_tooltip("glossary", GLOSSARY_TOOLTIPS, text)

    raise ValueError(f"Unhandled link: {tag}")


def make_tooltip(tooltip_type: str, tooltip_dict: dict, text: str) -> str:
    key = text.lower()
    if key in tooltip_dict:
        return f"[[{tooltip_type}:{text}]]"
    else:
        key = key.rstrip("s")
        if key in tooltip_dict:
            return f"[[{tooltip_type}:{key}|{text}]]"
        else:
            match text:
                case "Half Cover":
                    return f"[[tooltip:Half Cover]]"
                case "Three-Quarters Cover":
                    return f"[[tooltip:Three-Quarters Cover]]"
                case "Total Cover":
                    return f"[[tooltip:Total Cover]]"
                case "Short":
                    # Assume it means Short Rest
                    return f"[[glossary:Short Rest|Short]]"
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
    # We can just ignore some divs and pretend they don't exist
    output = []
    classes = parent.attrs["class"]
    if ("effect-info" in classes) or ("effects-info" in classes):
        return parse_ul(parent)
    ignorable_classes = ["subitems-list-details"]
    handled_classes = ["subitems-list-details-item"]
    sep = "\n"
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


if __name__ == "__main__":
    main()
    # a = """<a class="tooltip-hover skill-tooltip" data-tooltip-href="/skills/11-tooltip" href="/sources/dnd/free-rules/playing-the-game#Skills">Animal Handling</a>"""
    # b = bs4.BeautifulSoup(a, "html.parser")
    # print(parse_link(b.find()))
