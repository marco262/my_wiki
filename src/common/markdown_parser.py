"""
For parsing *.md files, including special handling of wiki code
"""
import re

from markdown2 import Markdown

EXTRAS = ["header-ids", "wiki-tables", "toc"]


class MarkdownParser:

    namespace = ""

    def __init__(self):
        self.markdown_obj = Markdown(extras=EXTRAS)
        self.markdown_obj.preprocess = self.pre_parsing

    def parse_md_path(self, path):
        with open(path) as f:
            return self.parse_md(f.read())

    def parse_md(self, text, namespace=""):
        self.namespace = namespace
        return self.markdown_obj.convert(text)

    def pre_parsing(self, text):
        text = self.convert_wiki_links(text)
        return text

    def convert_wiki_links(self, text):
        namespace_domain = "/" + self.namespace if self.namespace else ""
        # Convert wiki links to markdown
        # [[[class:cleric#toc|Table of Contents]]] -> [Table of Contents](/dnd/class/cleric#toc)
        text = re.sub(r"\[\[\[(.+?):(.+?)\|(.+?)\]\]\]", r"[\3](" + namespace_domain + r"/\1/\2)", text)
        # [[[class:cleric#domains]]] -> [domains](/dnd/class/cleric#domains)
        text = re.sub(r"\[\[\[(.+?):(.+?)#(.+?)\]\]\]", r"[\3](" + namespace_domain + r"/\1/\2#\3)", text)
        # [[[class:cleric]]] -> [cleric](/dnd/class/cleric)
        text = re.sub(r"\[\[\[(.+?):(.+?)\]\]\]", r"[\2](" + namespace_domain + r"/\1/\2)", text)
        # [[[Mutants]]] -> [Mutants](/numenera/mutants)
        text = re.sub(r"\[\[\[(.+?)\]\]\]", r"[\1](" + namespace_domain + r"/\1)", text)
        return text
