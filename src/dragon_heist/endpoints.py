from bottle import Bottle, template, view, redirect
from src.common.utils import md_page


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("home", "dragon_heist")

    @app.get("")
    @view("common/page.tpl")
    def calendar():
        return md_page("calendar", "dragon_heist", build_toc=False)

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "dragon_heist")
