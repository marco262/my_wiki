import re
from typing import Dict, TypedDict

from markdown2 import Markdown
from src.common.utils import title_to_page_name


class RulesGlossaryEntry(TypedDict):
    anchor: str
    content: str


def split_rules_glossary() -> Dict[str, RulesGlossaryEntry]:
    max_length = 500
    md = Markdown()
    with open("data/onednd/general/rules-glossary.md") as f:
        page = f.read()
    rules_glossary = {}
    split_page = re.split(r"^## ", page, flags=re.MULTILINE)
    for text in split_page:
        if not text:
            continue
        name, content = text.split("\n", maxsplit=1)
        anchor = title_to_page_name(name)
        m = re.match(r"^(.*) \[.*]$", name.lower())
        if m:
            name = m.group(1)
        if len(content) > max_length:
            content = content[:max_length] + " ... <em>[more]</em>"
        rules_glossary[name.lower()] = {
            "anchor": anchor,
            "content": md.convert(content).strip(" \n"),
        }
    return rules_glossary
