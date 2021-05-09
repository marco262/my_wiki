from importlib import import_module

from configparser import RawConfigParser

from bottle import Bottle

MODULE_NAMES = ["common", "dnd", "numenera", "dragon_heist", "waterdeep", "curse_of_strahd", "pirates"]


def load_wsgi_endpoints(app: Bottle, cfg: RawConfigParser):
    """
    Loads functions into the WSGI
    """
    for name in MODULE_NAMES:
        module = import_module("src.{}.endpoints".format(name))
        module.init(cfg)
        if name == "common":
            module.load_wsgi_endpoints(app)
        else:
            child_app = Bottle()
            module.load_wsgi_endpoints(child_app)
            app.mount("/" + name + "/", child_app)
