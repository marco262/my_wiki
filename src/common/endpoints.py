from urllib.parse import urljoin

from bottle import Bottle, view


def init(_cfg):
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("<path:path>")
    @view("redirect.tpl")
    def index_path(path):
        return {"site": urljoin(f"https://wiki.harebrained.dev", path)}
