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
    def general(name):
        return md_page(name, "onednd", "advancement")

    @app.get('/general/<name>')
    def general(name):
        return md_page(name, "onednd", "general")
