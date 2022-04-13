import bcrypt

from bottle import Bottle, view, auth_basic
from src.common.utils import md_page

# Default password: dancinglikeastripper
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

websocket_list = []


def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("Fin Fan!", "fin_fan")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "fin_fan")

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "fin_fan", directory="gm_notes")


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
