from importlib import import_module

MODULE_NAMES = ["general", "dnd", "numenera"]
MODULES = [import_module("src.endpoints." + name) for name in MODULE_NAMES]


def load_wsgi_endpoints():
    """
    Loads functions into the WSGI
    """
    for m in MODULES:
        m.init()

    for m in MODULES:
        m.load_wsgi_endpoints()
