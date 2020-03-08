from bottle import Bottle, template, view, redirect
from src.common.utils import md_page


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        redirect("/dragon_heist/GM Notes")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "dragon_heist")
