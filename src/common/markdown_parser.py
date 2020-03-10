"""
For parsing *.md files, including special handling of wiki code
"""
import re

from markdown2 import Markdown

EXTRAS = ["header-ids", "wiki-tables", "toc"]


class MarkdownParser:

    namespace = ""

    def __init__(self, init_md=True):
        # For unit testing
        if not init_md:
            self.markdown_obj = Markdown(extras=EXTRAS)
            self.markdown_obj.preprocess = self.pre_parsing

    def parse_md_path(self, path, namespace=""):
        with open(path) as f:
            file_contents = f.read()
        return self.parse_md(file_contents, namespace)

    def parse_md(self, text, namespace=""):
        self.namespace = namespace
        return self.markdown_obj.convert(text)

    def pre_parsing(self, text):
        text = self.convert_wiki_links(text)
        text = self.convert_popup_links(text)
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
        # [[[Mutants]]] -> [Mutants](/numenera/Mutants)
        text = re.sub(r"\[\[\[(.+?)\]\]\]", r"[\1](" + namespace_domain + r"/\1)", text)
        return text

    def convert_popup_links(self, text):
        pattern = r"\[\[popup (.*?)\]\](.*?)\[\[/popup\]\]"
        replace = r"""<a href="\1" target="popup" onclick="window.open('\1','popup','width=600,height=600', menubar=yes); return false;">\2</a>"""
        text = re.sub(pattern, replace, text)
        return text
