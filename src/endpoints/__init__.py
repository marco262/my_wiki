from importlib import import_module

from bottle import Bottle

MODULE_NAMES = ["general", "dnd", "numenera"]
MODULES = [import_module("src.endpoints." + name) for name in MODULE_NAMES]


def load_wsgi_endpoints(app: Bottle):
    """
    Loads functions into the WSGI
    """
    for m in MODULES:
        m.init()

    for m in MODULES:
        m.load_wsgi_endpoints(app)
