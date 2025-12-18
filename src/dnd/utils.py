import re
from re import finditer
from typing import TypedDict

from bs4 import BeautifulSoup, NavigableString, Tag
from markdown2 import Markdown
from src.common.utils import title_to_page_name, str_to_list

TOOLTIP_MAX_LENGTH = 500

class TooltipEntry(TypedDict):
    href: str
    content: str | list[str]

TooltipDict = dict[str, TooltipEntry]


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
            content = f"**Damage:** {cells[1]}  **Mastery:** {cells[3]}  **Weight:** {cells[4]}  **Cost:** {cells[5]}  \n**Properties:** {cells[2]}"
            href = "/dnd/general/Equipment#weapons"
        elif table_type == "Armor":
            content = f"**AC:** {cells[1]}  **Weight:** {cells[4]}  **Cost:** {cells[5]}"
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
