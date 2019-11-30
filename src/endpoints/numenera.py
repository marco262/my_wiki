import re
from html import unescape

from bottle import get, view, HTTPError, template

from src.markdown_parser import MarkdownParser

MD = None


def init():
    global MD
    MD = MarkdownParser()


def load_wsgi_endpoints():
    @get('/numenera')
    @view('numenera/page.tpl')
    def home():
        md = MD.parse_md_path("data/numenera/home.md")
        return {"title": "Numenera", "text": md, "toc": md.toc_html}

    @get('/numenera/Mutants_new')
    @view("numenera/page.tpl")
    def mutants():
        t = unescape(template("numenera/mutants.tpl"))
        md = MD.parse_md(t)
        return {"title": "Mutants", "text": md, "toc": md.toc_html}

    @get('/numenera/<name>')
    @view("numenera/page.tpl")
    def page(name):
        formatted_name = re.sub("\W", "-", name.lower())
        path = "data/numenera/" + formatted_name + ".md"
        try:
            md = MD.parse_md_path(path)
        except FileNotFoundError:
            raise HTTPError(404, f"I couldn't find \"{name}\".")
        return {"title": name.title(), "text": md, "toc": md.toc_html}
