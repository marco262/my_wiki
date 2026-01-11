"""
For parsing *.md files, including special handling of wiki code
"""
import os
import re
import tomllib
from tomllib import TOMLDecodeError
from typing import Dict

from bottle import template, TemplateError

from markdown2 import Markdown

from data.dnd.enums import custom_tooltips
from src.common.utils import title_to_page_name, list_media_files
from src.dnd5e.magic_item_tracker import build_magic_item_tracker
from src.dnd5e.npc_generator import create_npc
from src.dnd5e.utils import to_mod
from src.dnd.utils import TooltipEntry, TooltipDict, split_rules_glossary, split_equipment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXTRAS = [
    "header-ids", "wiki-tables", "toc", "strike", "task_list", "task_list_checkable", "tables", "markdown-in-html"
]


class MarkdownParser:
    namespace = ""
    accordion_text = False
    rules_glossary: Dict[str, TooltipEntry] = None
    tooltips: Dict[str, TooltipEntry] = None

    def __init__(self, check_for_broken_links=True, init_md=True):
        self.check_for_broken_links = check_for_broken_links
        # Disable for unit testing
        if init_md:
            self.markdown_obj = Markdown(extras=EXTRAS)
            self.markdown_obj.preprocess = self.pre_parsing
            self.markdown_obj.postprocess = self.post_parsing
            self.markdown_obj_with_metadata = Markdown(extras=EXTRAS + ["metadata"])
            self.markdown_obj_with_metadata.preprocess = self.pre_parsing
            self.markdown_obj_with_metadata.postprocess = self.post_parsing

    def parse_md_path(self, path, namespace=""):
        with open(path, encoding="utf-8") as f:
            file_contents = f.read()
        return self.parse_md(file_contents, namespace)

    def parse_md(self, text: str, namespace: str = "", with_metadata: bool = True, no_p: bool = False) -> str:
        """
        Parse Markdown text into HTML.

        Args:
            text (str): The Markdown text to be parsed.
            namespace (str, optional): The namespace for links and references. Defaults to "".
            with_metadata (bool, optional): Whether to parse Markdown as if it has a metadata header. Defaults to True.
            no_p (bool, optional): If True, removes surrounding <p> tags from the output. Defaults to False.

        Returns:
            str: The parsed HTML string.
        """
        self.namespace = namespace
        if with_metadata:
            md = self.markdown_obj_with_metadata.convert(text)
        else:
            md = self.markdown_obj.convert(text)
        if no_p:
            md = md[3:-5]
        return md

    def pre_parsing(self, text):
        text = self.convert_wiki_links(text)
        text = self.convert_popup_links(text)
        text = self.convert_simple_links(text)
        text = self.add_includes(text)
        text = self.add_breadcrumbs(text)
        text = self.insert_magic_item_trackers(text)
        return text

    def post_parsing(self, text):
        text = self.add_header_links(text)
        text = self.add_divs(text)
        text = self.parse_accordions(text)
        text = self.convert_wiki_divs(text)
        text = self.build_bibliography(text)
        text = self.convert_gm_notes_inserts(text)
        text = self.generate_npc_blocks(text)
        text = self.fancy_text(text)
        text = self.add_reference_tooltips(text)
        text = self.add_rules_glossary_tooltips(text)
        return text

    def convert_wiki_links(self, text):
        namespace_domain = "/" + self.namespace if self.namespace else ""
        for m in re.finditer(r"\[\[\[(?:(.+?):)?(.+?)(#(.+?))?(\|(.+?))?]]]", text):
            category = m.group(1)
            directory = namespace_domain + ("/" + category if category else "")
            filename = m.group(2).replace("/", "-")
            linkname = m.group(6) or m.group(4) or m.group(2)
            if m.group(4):
                anchor = "#" + title_to_page_name(m.group(4))
            else:
                anchor = ""
            broken_link = not (self.check_for_broken_links and self.check_for_md_file(directory, filename))
            classes = ["wiki-link" + (" broken" if broken_link else "")]
            if category:
                classes.append(category)
            class_names = " ".join(classes)
            text = text.replace(
                m.group(0),
                f'<a class="{class_names}" href="{directory}/{filename + anchor}">{linkname}</a>'
            )
        return text

    @staticmethod
    def check_for_md_file(directory, filename):
        filename = title_to_page_name(filename)
        path = os.path.join(BASE_DIR, "data", directory.lstrip("/"), filename)
        return os.path.isfile(path + ".md") or os.path.isfile(path + ".toml")

    # @staticmethod
    # def convert_popup_links(text):
    #     pattern = r"\[(.*?)]\(\^(.*?)\)"
    #     replace = r"""<a href="\2" target="popup" onclick="window.open('\2','popup','width=600,height=600', menubar=yes); return false;">\1</a>"""
    #     text = re.sub(pattern, replace, text)
    #     return text

    @staticmethod
    def convert_popup_links(text):
        # Convert visual aid links
        pattern = r"\[([^]]+?)]\(([\^\$])(.*?)\)"
        for m in re.finditer(pattern, text):
            if m.group(2) == "^":
                url = m.group(3)
                if not url.startswith("http"):
                    url = "/media/img/visual_aids/" + url
                hover_panel = f'<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="{url}"></span>'
                escaped_name = m.group(1).replace('"', "%22")
                replace = f'<span class="visual-aid-link" title="visual_aid|{m.group(3)}|{escaped_name}">{m.group(1)}{hover_panel}</span>'
            elif m.group(2) == "$":
                replace = f'<span class="visual-aid-link" title="{m.group(3)}">{m.group(1)}</span>'
            else:
                raise ValueError(f"Unknown link flag: {m.group(2)}")
            text = text.replace(m.group(0), replace)
        # Convert popup links
        pattern = r"\[([^]]+?)]\(([\@])(.*?)\)"
        for m in re.finditer(pattern, text):
            url = m.group(3)
            if not url.startswith("http"):
                url = "/media/img/visual_aids/" + url
            hover_panel = f'<span class="visual-aid-hover"><img class="visual-aid-hover-img" src="{url}"></span>'
            replace = f'<a href="{url}" class="popup-link" target="_blank">{m.group(1)}{hover_panel}</a>'
            text = text.replace(m.group(0), replace)
        return text

    @staticmethod
    def convert_simple_links(text):
        """
        Finds links with format [text]() and fills them out with [text](text).
        Finds links with format [This is Text](#) and fills them out with [This is Text](#this-is-text).
        Useful for quick links to markdown files in the same folder, and anchors on the same page.
        """
        for m in re.finditer(r"\[([^\[]+)]\((#?)\)", text):
            if m.group(2) == "#":
                text = text.replace(m.group(0), f"[{m.group(1)}](#{title_to_page_name(m.group(1))})")
            else:
                text = text.replace(m.group(0), f"[{m.group(1)}]({m.group(1)})")
        return text

    def add_includes(self, text):
        for m in re.finditer(r'\[\[include (.*?)]]((.*?)\[\[/include]])?', text, re.DOTALL):
            template_name = m.group(1)
            args = {}
            # If the whole include block was defined, including end tag, parse inner arguments
            if m.group(3):
                # Split inner arguments into rows
                content = m.group(3).strip("\n")
                rows = content.split("\n")
                index = 0
                # Iterate through all inner arguments and parse each individually
                # Some arguments might span multiple rows, so we want to handle indexing manually
                while index < len(rows):
                    arg = rows[index].strip()
                    # Skip blank lines
                    if not arg:
                        index += 1
                        continue
                    # print(arg)
                    try:
                        k, v = arg.split("=", 1)
                    except ValueError:
                        raise ValueError("Can't split line: {!r}".format(arg))
                    k, v = k.strip(), v.strip()
                    if k == "file":
                        # Load a toml file, and add each value from that file to args individually
                        # Parse markdown as necessary
                        path = os.path.join("data", v)
                        try:
                            with open(path) as f:
                                toml_dict = tomllib.loads(f.read())
                        except tomllib.TOMLDecodeError as e:
                            raise TOMLDecodeError(f"Couldn't decode '{path}'") from e
                        for k, v in toml_dict.items():
                            if isinstance(v, str) and v.startswith("!"):
                                v = self.parse_md(v[1:].strip("\n"), namespace=self.namespace, with_metadata=False)
                            args[k] = v
                    elif k == "glob":
                        # Useful for lightgallery
                        args["glob_file_list"] = ["/" + path for path in list_media_files(v.strip())]
                    elif v.startswith("!!!"):
                        # Parse all text between the !!! and the next !!! as one block of markdown
                        # First gather the entire block into one string
                        full_value = v[3:] + "\n"
                        while index < len(rows):
                            index += 1
                            row = rows[index]
                            if row.endswith("!!!"):
                                full_value += row[:-3]
                                break
                            full_value += row + "\n"
                        else:
                            raise ValueError(f"Ran out of data while looking for closing !!! "
                                             f"(template_name={template_name}, key={k})")
                        # Parse that whole string as markdown
                        v = self.parse_md(full_value.strip(" \n"), namespace=self.namespace, with_metadata=False)
                    elif v.startswith("!"):
                        # Parse a single line as markdown
                        v = self.parse_md(v[1:].replace(r"\n", "\n"), namespace=self.namespace, with_metadata=False)
                    args[k] = v
                    index += 1
            # print(args)
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
        m = re.search(r"\[\[breadcrumb (.*?)\|(.*?)]]", text)
        if m:
            return text.replace(m.group(0), f"\u27F5 [{m.group(2)}]({m.group(1)})")
        return text

    @staticmethod
    def insert_magic_item_trackers(text):
        pattern = r"\[\[magic-item-tracker]](.*?)\[\[/magic-item-tracker]]"
        for m in re.finditer(pattern, text, re.DOTALL):
            magic_items = m.group(1).strip("\n")
            magic_item_tracker_table = build_magic_item_tracker(magic_items)
            new_text = f"{magic_items}\n\n{magic_item_tracker_table}"
            new_text += "\n\n*Reference: [Magic Items](/dnd/dm_toolbox/Magic Items)*"
            text = text.replace(m.group(0), new_text)
        return text

    def add_reference_tooltips(self, text: str) -> str:
        if not self.tooltips:
            self.tooltips = split_equipment()
            self.tooltips.update(custom_tooltips)
        return self._add_tooltip(self.tooltips, r"\[\[tooltip:(.*?)(\|(.*?))?\]\]", text)

    def add_rules_glossary_tooltips(self, text: str) -> str:
        if not self.rules_glossary:
            self.rules_glossary = split_rules_glossary()
        return self._add_tooltip(self.rules_glossary, r"\[\[glossary:(.*?)(\|(.*?))?\]\]", text)

    @staticmethod
    def _add_tooltip(tooltip_dict: TooltipDict, pattern: str, text: str) -> str:
        tooltip_fmt = '<dfn name="{name}"><button class="dfn-tooltip" href="{href}">{content}</button></dfn>'
        for m in re.finditer(pattern, text):
            try:
                g = tooltip_dict[m.group(1).lower()]
            except KeyError:
                # raise KeyError(f"Invalid tooltip entry '{m.group(1)}'. match={m.group(0)}")
                print(f"Invalid tooltip entry '{m.group(1)}'. match={m.group(0)}")
                tooltip_fmt = '<dfn class="broken" name="{name}"><button class="dfn-tooltip" href=""></button></dfn>'
                tooltip = tooltip_fmt.format(name=m.group(3) or m.group(1))
            else:
                # Avoid including pipes (|) so we don't screw up tables
                content = g["content"].split("|")[0].strip()
                tooltip = tooltip_fmt.format(
                    name=m.group(3) or m.group(1),
                    href=g["href"],
                    content=content,
                )
            text = text.replace(m.group(0), tooltip)
        return text

    @staticmethod
    def add_header_links(text):
        for m in re.finditer(r'(<h\d id="(.*?)".*?)(</h\d>)', text):
            text = text.replace(
                m.group(0),
                f'{m.group(1)}<a href="#{m.group(2)}" class="header-link">¶</a>{m.group(3)}'
            )
        return text

    def add_divs(self, text: str) -> str:
        text = text.replace("[[sidebar]]", '<div class="phb-sidebar" markdown="1">')
        text = text.replace("[[errata]]", '<div class="errata" markdown="1">')
        text = text.replace("[[homebrew]]", '<div class="homebrew-note" markdown="1">')
        text = text.replace("[[/sidebar]]", "</div>")
        text = text.replace("[[/errata]]", "</div>")
        text = text.replace("[[/homebrew]]", "</div>")
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

    @staticmethod
    def convert_gm_notes_inserts(text):
        for m in re.finditer(r"<p>\[\[gm_notes(.*?)]]</p>", text):
            name = m.group(1).strip(" ")
            element_id = title_to_page_name(name)
            text = text.replace(
                m.group(0),
                f"""<details class="gm-notes" id="{element_id}">
    <summary>GM Notes for {name}</summary>
</details>"""
            )
        return text

    def generate_npc_blocks(self, text):
        for m in re.finditer(r"\[\[npc (.*?)]]", text):
            # Fix issue where markdown may have converted underscores to <em> tags
            group_1 = re.sub(r"</?em>", "_", m.group(1))
            d = dict([x.split("=") for x in group_1.split("|")])
            npc = create_npc(**d)
            npc["width"] = d.get("width", "400px")
            npc["untrained"] = to_mod(npc["stat_bonus"])
            npc["proficient"] = to_mod(npc["stat_bonus"] + npc["prof_bonus"])
            npc["expertise"] = to_mod(npc["stat_bonus"] + npc["prof_bonus"] * 2)
            weapon_attack = \
                f"***{d.get('weapon', 'Weapon attack')} x{npc['num_attacks']}.*** {to_mod(npc['attack'])} to hit. " \
                f"**Hit:** {npc['damage']} damage.\n\n"
            if "actions" in npc:
                npc["actions"].insert(0, weapon_attack)
            else:
                npc["actions"] = [weapon_attack]
            for section in ["special_abilities", "bonus_actions", "actions", "reactions", "villain_actions"]:
                npc[section] = self.parse_md("\n\n".join(npc[section]), with_metadata=False) if npc[section] else ""
            t = template("dnd/npc-sheet.tpl", **npc)
            text = text.replace(m.group(0), t)
        return text

    @staticmethod
    def fancy_text(text):
        text = re.sub(r"(?<!-)--(?!-)", "&mdash;", text)
        return text


DEFAULT_MARKDOWN_PARSER = MarkdownParser()
