"""
For parsing *.md files, including special handling of wiki code
"""
import os
import re

import toml
from bottle import template, TemplateError
from markdown2 import Markdown

from src.common.utils import title_to_page_name

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXTRAS = ["header-ids", "wiki-tables", "toc", "strike"]


class MarkdownParser:
    namespace = ""
    accordion_text = False

    def __init__(self, check_for_broken_links=True, init_md=True):
        self.check_for_broken_links = check_for_broken_links
        # Disable for unit testing
        if init_md:
            self.markdown_obj = Markdown(extras=EXTRAS)
            self.markdown_obj.preprocess = self.pre_parsing
            self.markdown_obj.postprocess = self.post_parsing

    def parse_md_path(self, path, namespace=""):
        with open(path, encoding="utf-8") as f:
            file_contents = f.read()
        return self.parse_md(file_contents, namespace)

    def parse_md(self, text, namespace=""):
        self.namespace = namespace
        return self.markdown_obj.convert(text)

    def pre_parsing(self, text):
        text = self.convert_wiki_links(text)
        text = self.convert_popup_links(text)
        text = self.add_includes(text)
        text = self.add_breadcrumbs(text)
        return text

    def post_parsing(self, text):
        text = self.add_header_links(text)
        text = self.parse_accordions(text)
        text = self.convert_wiki_divs(text)
        text = self.build_bibliography(text)
        return text

    def convert_wiki_links(self, text):
        namespace_domain = "/" + self.namespace if self.namespace else ""
        for m in re.finditer(r"\[\[\[((.+?):)?(.+?)(#(.+?))?(\|(.+?))?]]]", text):
            groups = m.groups()
            directory = namespace_domain + ("/" + groups[1] if groups[1] else "")
            filename = groups[2].replace("/", "-")
            linkname = groups[6] or groups[4] or groups[2]
            broken_link = not (self.check_for_broken_links and self.check_for_md_file(directory, filename))
            class_name = "wiki-link" + ("-broken" if broken_link else "")
            text = text.replace(
                m.group(0),
                f'<a class="{class_name}" href="{directory}/{filename + (groups[3] or "")}">{linkname}</a>'
            )
        return text

    @staticmethod
    def check_for_md_file(dir, filename):
        filename = title_to_page_name(filename)
        path = os.path.join(BASE_DIR, "data", dir.lstrip("/"), filename)
        # print(path)
        return os.path.isfile(path + ".md") or os.path.isfile(path + ".toml")

    # @staticmethod
    # def convert_popup_links(text):
    #     pattern = r"\[(.*?)]\(\^(.*?)\)"
    #     replace = r"""<a href="\2" target="popup" onclick="window.open('\2','popup','width=600,height=600', menubar=yes); return false;">\1</a>"""
    #     text = re.sub(pattern, replace, text)
    #     return text

    @staticmethod
    def convert_popup_links(text):
        pattern = r"\[([^]]+?)]\(([\^\$])(.*?)\)"
        for m in re.finditer(pattern, text):
            if m.group(2) == "^":
                hover_panel = f'<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="/static/img/visual_aids/{m.group(3)}"></span>'
                replace = f'<span class="visual-aid-link" title="visual_aid|{m.group(3)}">{m.group(1)}{hover_panel}</span>'
            elif m.group(2) == "$":
                replace = f'<span class="visual-aid-link" title="{m.group(3)}">{m.group(1)}</span>'
            else:
                raise ValueError(f"Unknown link flag: {m.group(2)}")
            text = text.replace(m.group(0), replace)
        return text

    def add_includes(self, text):
        for m in re.finditer(r'\[\[include (.*?)]]((.*?)\[\[/include]])?', text, re.DOTALL):
            template_name = m.group(1)

            args = {}
            if m.group(3):
                content = m.group(3).strip("\n")
                rows = content.split("\n")
                index = 0
                while index < len(rows):
                    arg = rows[index]
                    try:
                        k, v = arg.split("=", 1)
                    except ValueError:
                        raise ValueError("Can't split line: " + arg)
                    k, v = k.strip(), v.strip()
                    if k == "file":
                        toml_dict = toml.load(os.path.join("data", v))
                        for k, v in toml_dict.items():
                            if isinstance(v, str) and v.startswith("!"):
                                v = self.parse_md(v[1:].strip("\n"), namespace=self.namespace)
                            args[k] = v
                    elif v.startswith("!!!"):
                        # Gather the remaining lines
                        full_value = v[3:] + "\n"
                        while True:
                            index += 1
                            row = rows[index]
                            if row.endswith("!!!"):
                                full_value += row[:-3]
                                break
                            full_value += row + "\n"
                        v = self.parse_md(full_value.strip(" \n"), namespace=self.namespace)
                    elif v.startswith("!"):
                        v = self.parse_md(v[1:].replace(r"\n", "\n"), namespace=self.namespace)
                    args[k] = v
                    index += 1

            if template_name.endswith(".tpl"):
                try:
                    t = template(template_name, args)
                except TemplateError:
                    raise TemplateError(f"Can't find template: {template_name}")
                except NameError:
                    print(f"Error when processing {template_name}")
                    raise
            elif template_name.endswith(".md"):
                t = self.parse_md_path(os.path.join("data", template_name), namespace=self.namespace)
            else:
                raise ValueError("Unknown file: {}".format(template_name))

            text = text.replace(m.group(0), t)
        return text

    @staticmethod
    def add_breadcrumbs(text):
        m = re.match(r"\[\[breadcrumb (.*?)\|(.*?)]]", text)
        if m:
            return text.replace(m.group(0), f"\u27F5 [{m.group(2)}]({m.group(1)})")
        return text

    @staticmethod
    def add_header_links(text):
        for m in re.finditer(r'(<h\d id="(.*?)".*?)(<\/h\d>)', text):
            text = text.replace(m.group(0),
                                f'{m.group(1)}<a href="#{m.group(2)}" class="header-link">¶</a>{m.group(3)}')
        return text

    def parse_accordions(self, text):
        self.accordion_text = False
        for m in re.finditer(r".*\[\[accordion (.*?)]].*", text):
            self.accordion_text = True
            text = text.replace(
                m.group(0),
                f'<button class="accordion-button">{m.group(1)}</button>\n<div class="accordion-panel">'
            )
        text = re.sub(r".*\[\[/accordion]].*", "</div>", text)
        return text

    @staticmethod
    def convert_wiki_divs(text):
        text = re.sub(r"<p>\[\[div(.*?)]]</p>", r"<div\1>", text)
        text = re.sub(r"<p>\[\[/div]]</p>", r"</div>", text)
        text = re.sub(r"\[\[span(.*?)]]", r"<span\1>", text)
        text = re.sub(r"\[\[/span]]", r"</span>", text)
        text = re.sub(r"<p>\[\[clear-float]]</p>", r'<div class="clear-float"></div>', text)
        return text

    @staticmethod
    def build_bibliography(text):
        pattern = r"\[\[bibliography]](.*?)\[\[/bibliography]]"
        m = re.search(pattern, text, re.DOTALL)
        if m:
            bib_list = []
            cite_find_format = "[((bibcite {}))]"
            cite_replace_format = '[<a href="#{}">{}</a>]'
            bib_format = '    <li><a id="{}" />{}</li>'
            for i, line in enumerate(m.group(1).strip("\n").split("\n")):
                split_line = line.split(":", 2)
                name = split_line[1].strip(" ")
                text = text.replace(cite_find_format.format(name), cite_replace_format.format(name, i + 1))
                bib_list.append(bib_format.format(name, split_line[2].strip(" ")))
            text = text.replace(m.group(0),
                                "<p><strong>Bibliography</strong></p>\n\n<ol>\n{}\n</ol>".format("\n".join(bib_list)))

        return text


DEFAULT_MARKDOWN_PARSER = MarkdownParser()
