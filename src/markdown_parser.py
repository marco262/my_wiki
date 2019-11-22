"""
For parsing *.md files, including special handling of wiki code
"""
import re

from markdown2 import Markdown

EXTRAS = ["header-ids", "wiki-tables"]


class MarkdownParser:

    def __init__(self):
        self.markdown_obj = Markdown(extras=EXTRAS)

    def parse_md_path(self, path):
        with open(path) as f:
            return self.parse_md(f.read())

    def parse_md(self, text):
        text = self.pre_parsing(text)
        text = self.markdown_obj.convert(text)
        return self.post_parsing(text)

    def pre_parsing(self, text):
        text = self.convert_wiki_links(text)
        return text

    @staticmethod
    def convert_wiki_links(text):
        # Convert wiki links to markdown
        # [[[class:cleric#toc|Table of Contents]]] -> [Table of Contents](/class/cleric#toc)
        text = re.sub(r"\[\[\[(.+?):(.+?)\|(.+?)\]\]\]", r"[\3](/\1/\2)", text)
        # [[[class:cleric#domains]]] -> [domains](/class/cleric#domains)
        text = re.sub(r"\[\[\[(.+?):(.+?)#(.+?)\]\]\]", r"[\3](/\1/\2#\3)", text)
        # [[[class:cleric]]] -> [cleric](/class/cleric)
        text = re.sub(r"\[\[\[(.+?):(.+?)\]\]\]", r"[\2](/\1/\2)", text)
        return text

    def post_parsing(self, text):
        return text
