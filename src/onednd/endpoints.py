from bottle import Bottle

from src.common.utils import md_page


def init(cfg):
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    def home():
        return md_page("One D&D Wiki", "onednd", build_toc=False)

    # Categories

    @app.get('/advancement/<name>')
    def advancement(name):
        return md_page(name, "onednd", "advancement")

    @app.get('/class/<name>')
    def dnd_class(name):
        return md_page(name, "onednd", "class")

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "onednd", "general")

    @app.get('/subclass/<name>')
    def subclass(name):
        return md_page(name, "onednd", "subclass")
