import bcrypt
from bottle import Bottle, view, auth_basic

from src.common.utils import md_page
from src.class_1a.calendar import generate_months

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
        return md_page("Class 1A", "class_1a", build_toc=False, title="Class 1A")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "class_1a")

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "class_1a", directory="gm_notes")

    @app.get("<category:path>/<name>")
    @view("common/page.tpl")
    def category_page(category, name):
        return md_page(name, "class_1a", directory=category)

    @app.get("/calendar_old")
    @view("sandpoint/calendar_old.tpl")
    def calendar_old():
        return

    @app.get("/calendar")
    @view("sandpoint/calendar.tpl")
    def calendar():
        months = {y: m for y, m in generate_months(1495, "Rova", 4707, "Lamashan")}
        return {"months": months}


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
