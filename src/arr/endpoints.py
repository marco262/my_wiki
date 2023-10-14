from glob import glob

import bcrypt
from bottle import Bottle, view, auth_basic

from src.common.utils import md_page, list_media_files

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
        return md_page("A Realm Reborn", "arr")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "arr")

    @app.get("gm_notes/soundboard")
    @view("arr/soundboard.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes():
        g = [f.replace("\\", "/").replace("media/audio/arr/", "")
             for f in list_media_files("media/audio/arr/*.*")]
        return {"glob_file_list": g}

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "arr", directory="gm_notes")

    @app.get("gm_notes/insert/<name>")
    @auth_basic(gm_notes_auth_check)
    def gm_notes_insert(name):
        return md_page(name, "arr", directory="gm_notes/inserts", load_template=False)

    @app.get("<category:path>/<name>")
    @view("common/page.tpl")
    def category_page(category, name):
        return md_page(name, "arr", directory=category)


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
