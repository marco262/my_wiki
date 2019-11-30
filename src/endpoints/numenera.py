import re
from html import unescape
from os.path import isfile

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

    @get('/numenera/<name>')
    @view("numenera/page.tpl")
    def page(name):
        formatted_name = re.sub("\W", "-", name.lower())
        if isfile(f"views/numenera/{formatted_name}.tpl"):
            text = unescape(template(f"views/numenera/{formatted_name}.tpl"))
        elif isfile(f"data/numenera/{formatted_name}.md"):
            with open(f"data/numenera/{formatted_name}.md") as f:
                text = f.read()
        else:
            raise HTTPError(404, f"I couldn't find \"{name}\".")
        md = MD.parse_md(text)
        return {"title": name.title(), "text": md, "toc": md.toc_html}
