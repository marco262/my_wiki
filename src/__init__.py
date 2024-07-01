from importlib import import_module

from configparser import RawConfigParser

from bottle import Bottle

MODULE_NAMES = [
    "common", "dnd", "onednd", "numenera", "dragon_heist", "waterdeep", "curse_of_strahd", "pirates", "arr",
    "sandpoint", "class_1a"
]


def load_wsgi_endpoints(app: Bottle, cfg: RawConfigParser):
    """
    Loads functions into the WSGI
    """
    for name in MODULE_NAMES:
        # Load normal endpoints
        module = import_module("src.{}.endpoints".format(name))
        module.init(cfg)
        if name == "common":
            module.load_wsgi_endpoints(app)
        else:
            child_app = Bottle()
            module.load_wsgi_endpoints(child_app)
            app.mount(f"/{name}/", child_app)
        # Load API
        try:
            module = import_module("src.{}.api".format(name))
        except ModuleNotFoundError:
            pass
        else:
            child_app = Bottle()
            module.load_api_endpoints(child_app)
            app.mount(f"/api/{name}/", child_app)
