import bcrypt
from bottle import Bottle, view, auth_basic

from src.common.utils import md_page

# Default password: dancinglikeastripper
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"


def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("Curse of Strahd", "curse_of_strahd")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "curse_of_strahd")

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "curse_of_strahd", directory="gm_notes")

    @app.get("")
    @view("common/page.tpl")
    def calendar():
        return md_page("calendar", "curse_of_strahd", build_toc=False)

    @app.get("tarokka")
    @view("curse_of_strahd/tarokka.tpl")
    def calendar():
        return


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
