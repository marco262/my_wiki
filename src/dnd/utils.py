import re
from typing import TypedDict

from markdown2 import Markdown
from src.common.utils import title_to_page_name, str_to_list


class TooltipEntry(TypedDict):
    href: str
    content: str

TooltipDict = dict[str, TooltipEntry]


def split_rules_glossary() -> TooltipDict:
    max_length = 500
    md = Markdown()
    with open("data/dnd/general/rules-glossary.md") as f:
        page = f.read()
    rules_glossary = {}
    split_page = re.split(r"^## ", page, flags=re.MULTILINE)
    for text in split_page[1:]:
        if not text:
            continue
        name, content = text.split("\n", maxsplit=1)
        href = title_to_page_name(name)
        m = re.match(r"^(.*) \[.*]$", name.lower())
        if m:
            name = m.group(1)
        if len(content) > max_length:
            content = content[:max_length] + " ... <em>[more]</em>"
        rules_glossary[name.lower()] = {
            "href": "/dnd/general/Rules Glossary#" + href,
            "content": md.convert(content).strip(" \n"),
        }
    return rules_glossary


def split_equipment() -> TooltipDict:
    max_length = 500
    md = Markdown()
    with open("data/dnd/general/equipment.md") as f:
        page = f.read()
    tooltips = {}
    save_text = False
    table_type = None
    key = ""
    lines = page.split("\n")
    for line in lines:
        if not line:
            continue
        if line.startswith("## "):
            if line in ("## Properties", "## Mastery Properties", "## Artisan's Tools", "## Other Tools", "## Adventuring Gear"):
                save_text = True
                table_type = False
            elif line == "## Weapons":
                save_text = True
                table_type = "Weapons"
            elif line == "## Armor":
                save_text = True
                table_type = "Armor"
            else:
                save_text = False
            key = ""
            continue
        if save_text:
            if table_type in ("Weapons", "Armor"):
                if line.startswith("|"):
                    text = line.replace("[[tooltip:", "").replace("]]", "")
                    cells = str_to_list(text, delimiter="|")
                    key = cells[0].lower()
                    if key == "name" or key.startswith("---"):
                        continue

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

                    tooltips[key] = {
                        "href": "/dnd/general/Equipment#" + href,
                        "content": [content],
                    }
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
        if len(content) > max_length:
            content = content[:max_length] + " ... <em>[more]</em>"
        d["content"] = content

    return tooltips
