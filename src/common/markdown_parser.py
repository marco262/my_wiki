"""
For parsing *.md files, including special handling of wiki code
"""
import os
import re

from markdown2 import Markdown

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXTRAS = ["header-ids", "wiki-tables", "toc"]


class MarkdownParser:

    namespace = ""

    def __init__(self, check_for_broken_links=True, init_md=True):
        self.check_for_broken_links = check_for_broken_links
        # Disable for unit testing
        if init_md:
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
        if self.check_for_broken_links:
            text = self.check_wiki_links(text)
        text = self.convert_popup_links(text)
        return text

    def convert_wiki_links(self, text):
        namespace_domain = "/" + self.namespace if self.namespace else ""
        # Convert wiki links to markdown
        # [[[class:cleric#toc|Table of Contents]]] -> [Table of Contents](/dnd/class/cleric#toc)
        text = re.sub(
            r"\[\[\[(.+?):(.+?)\|(.+?)\]\]\]",
            r'<a class="wiki-link" href="{}/\1/\2">\3</a>'.format(namespace_domain),
            text
        )
        # [[[class:cleric#domains]]] -> [domains](/dnd/class/cleric#domains)
        text = re.sub(
            r"\[\[\[(.+?):(.+?)#(.+?)\]\]\]",
            r'<a class="wiki-link" href="{}/\1/\2#\3">\3</a>'.format(namespace_domain),
            text
        )
        # [[[class:cleric]]] -> [cleric](/dnd/class/cleric)
        text = re.sub(
            r"\[\[\[(.+?):(.+?)\]\]\]",
            r'<a class="wiki-link" href="{}/\1/\2">\2</a>'.format(namespace_domain),
            text
        )
        # [[[Mutants]]] -> [Mutants](/numenera/Mutants)
        text = re.sub(
            r"\[\[\[(.+?)\]\]\]",
            r'<a class="wiki-link" href="{}/\1">\1</a>'.format(namespace_domain),
            text
        )
        return text

    def check_wiki_links(self, text):
        """
        Finds links of the form <a class="wiki-link" href="{url}">{name}</a> and checks if their {url} is a valid
        path for a markdown document in the /data/ directory of this project. If not, it changes the "wiki-link"
        class to "wiki-link-broken".
        """
        for m in re.finditer(r'<a class="wiki-link" href="(.*?)">.*?</a>', text):
            url = m.group(1).split("#")[0]
            if not self.check_for_md_file(url):
                text = text.replace(m.group(0), m.group(0).replace('class="wiki-link"', 'class="wiki-link-broken"'))
        return text

    @staticmethod
    def check_for_md_file(path):
        path = os.path.join(BASE_DIR, "data", path.lstrip("/") + ".md")
        # print(path)
        return os.path.isfile(path)

    @staticmethod
    def convert_popup_links(text):
        pattern = r"\[\[popup (.*?)\]\](.*?)\[\[/popup\]\]"
        replace = r"""<a href="\1" target="popup" onclick="window.open('\1','popup','width=600,height=600', menubar=yes); return false;">\2</a>"""
        text = re.sub(pattern, replace, text)
        return text
