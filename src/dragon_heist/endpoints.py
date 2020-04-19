from json import dumps

import bcrypt

from bottle import Bottle, view, request, response, redirect, auth_basic
from src.common.utils import md_page

visual_aid_url = "/static/img/dnd_party.png"
set_visual_aid_hash = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("home", "dragon_heist")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "dragon_heist")

    @app.get("")
    @view("common/page.tpl")
    def calendar():
        return md_page("calendar", "dragon_heist", build_toc=False)

    @app.get("visual_aid")
    @view("dragon_heist/visual_aid.tpl")
    def visual_aid():
        return

    @app.get("get_visual_aid")
    def get_visual_aid():
        global visual_aid_url
        response.content_type = 'application/json'
        return dumps({"url": visual_aid_url})

    @app.get("set_visual_aid")
    @auth_basic(set_visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_url
        url = request.params["url"]
        print("Saved new URL: {!r}".format(url))
        visual_aid_url = url
        if request.params.get("redirect") != "false":
            redirect(url)


def set_visual_aid_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), set_visual_aid_hash)
