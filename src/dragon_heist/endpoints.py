from json import dumps

import bcrypt
from bottle_websocket import websocket
from gevent import sleep
from geventwebsocket import WebSocketError

from bottle import Bottle, view, request, response, redirect, auth_basic
from src.common.utils import md_page

visual_aid_url = "/static/img/visual_aids/dnd_party.png"
set_visual_aid_hash = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"
websocket_list = []


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

    @app.get('/get_visual_aid', apply=[websocket])
    def get_visual_aid(ws):
        global visual_aid_url, websocket_list
        print("Opening Websocket {}".format(ws))
        websocket_list.append(ws)
        try:
            ws.send(dumps({"url": visual_aid_url}))
            while True:
                sleep(60)
        except WebSocketError:
            print("Closing Websocket {}".format(ws))
            websocket_list.remove(ws)

    @app.get("set_visual_aid")
    @auth_basic(set_visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_url, websocket_list
        url = request.params["url"]
        # Support for locally hosted files
        if not url.startswith("http"):
            url = "/static/img/visual_aids/" + url
        print("Saved new URL: {!r}".format(url))
        visual_aid_url = url
        # Update WebSockets
        print(websocket_list)
        for websocket in websocket_list[:]:
            try:
                print("Sending new URL to {}".format(websocket))
                websocket.send(dumps({"url": visual_aid_url}))
            except WebSocketError:
                print("Failed to send message to {}. Removing from list".format(websocket))
                websocket_list.remove(websocket)
        if request.params.get("redirect") != "false":
            redirect(url)


def set_visual_aid_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), set_visual_aid_hash)
