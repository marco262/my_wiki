"""
Copy the HTML content from D&D Beyond into a file (no nav bar, no header, etc.), and put that file's path in PATH.
This script will then convert that file into a Markdown representation of that file.
It will also add a "Source:" section at the end. Make sure to fill that out manually using a real book reference
like "Player's Handbook, p. 34".
"""

import bs4
from bs4 import Tag, NavigableString

from data.dnd.enums import tooltips

PATH = "../data/dnd/class/barbarian.md"


def main() -> None:
    # Load the HTML file into Beautiful Soup
    with open(PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = bs4.BeautifulSoup(html_content, "html.parser")

    output = []
    for tag in soup:  # type: Tag
        if isinstance(tag, NavigableString):
            continue
        output.append(parse_tag(tag))
    output = "\n\n".join(output)

    # Replace "smart" quotes
    output = output.replace("’", "'")

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
            return parse_tag(parent.find())
        case "div":
            return parse_div(parent)

    output = []
    for tag in parent:  # type: Tag
        match tag.name:
            case None:
                text = tag.get_text()
                if text and text != "\n":
                    output.append(text)
            case "strong":
                text = parse_tag(tag)
                output.append(f"**{text}**")
            case "em":
                text = parse_tag(tag)
                output.append(f"_{text}_")
            case "a":
                output.append(parse_link(tag))
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
    """
    Convert a Beautiful Soup <table> element to a Markdown table string.
    Assumes the first row contains headers (using <th> or <td>).
    """
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
        should_bold_text = False
        # Sometimes we have "sideways" tables, where there's no header
        # but the left column is bolded. This is to handle that case by bolding
        # the text in the <th> cells.
        match cell.name:
            case "th":
                if not header:
                    should_bold_text = True
        if should_bold_text:
            cell_text_list.append(f"**{cell_text}**")
        else:
            cell_text_list.append(cell_text)
    output = [markdown_row(cell_text_list)]
    if header:
        output.append(markdown_header_sep(len(cell_text_list)))
    return output


def markdown_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def markdown_header_sep(num_cells: int) -> str:
    return "|" + "|".join(["---"] * num_cells) + "|"


def parse_link(tag: Tag) -> str:
    classes = tag.attrs["class"]
    if "spell-tooltip" in classes:
        return f"_[[[spell:{tag.get_text()}]]]"
    tooltip_classes = ["skill-tooltip", "item-tooltip", "weapon-properties-tooltip"]
    for c in tooltip_classes:
        if c in classes:
            text = tag.get_text()
            key = text.lower()
            if key in tooltips:
                return f"[[tooltip:{text}]]"
            else:
                key = key.rstrip("s")
                if key in tooltips:
                    return f"[[tooltip:{key}|{text}]]"
                else:
                    raise ValueError(f"Undefined tooltip: {text}")
    glossary_classes = ["condition-tooltip", "action-tooltip", "rule-tooltip", "sense-tooltip"]
    for c in glossary_classes:
        if c in classes:
            return f"[[glossary:{tag.get_text()}]]"
    raise ValueError(f"Unhandled link: {tag}")


def parse_ul(parent: Tag) -> str:
    output = []
    for tag in parent:  # type: Tag
        if isinstance(tag, NavigableString):
            continue
        assert tag.name == "li"
        output.append(" - " + parse_tag(tag))
    return "\n".join(output)


def parse_div(parent: Tag) -> str:
    # We can just ignore some divs and pretend they don't exist
    output = []
    classes = parent.attrs["class"]
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
