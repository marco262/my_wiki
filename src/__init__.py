from importlib import import_module

from bottle import Bottle
from src.common.markdown_parser import MarkdownParser

MD = MarkdownParser()

MODULE_NAMES = ["common", "dnd", "numenera"]


def load_wsgi_endpoints(app: Bottle):
    """
    Loads functions into the WSGI
    """
    for name in MODULE_NAMES:
        module = import_module("src.{}.endpoints".format(name))
        module.init()
        if name == "common":
            module.load_wsgi_endpoints(app)
        else:
            child_app = Bottle()
            module.load_wsgi_endpoints(child_app)
            app.mount("/" + name + "/", child_app)
