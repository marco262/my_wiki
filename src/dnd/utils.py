import re
from typing import TypedDict

from markdown2 import Markdown
from src.common.utils import title_to_page_name


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
    for text in split_page:
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
