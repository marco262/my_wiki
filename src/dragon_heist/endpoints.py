from json import dumps

import bcrypt
import gevent
from bottle_websocket import websocket
from gevent import sleep
from geventwebsocket import WebSocketError

from bottle import Bottle, view, request, redirect, auth_basic
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
        return md_page("Dragon Heist", "dragon_heist")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "dragon_heist")

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(set_visual_aid_auth_check)
    def gm_notes(name):
        return md_page(name, "dragon_heist", directory="gm_notes")

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
        print("Opening Websocket {}".format(ws), flush=True)
        websocket_list.append(ws)
        try:
            ws.send(dumps({"url": visual_aid_url}))
            while True:
                sleep(60)
                # Checking if websocket has been closed by the client
                with gevent.Timeout(1.0, False):
                    ws.receive()
                if ws.closed:
                    print("WebSocket was closed by the client: {}".format(ws), flush=True)
                    break
        except Exception as e:
            print("Error in WebSocket loop: {}".format(e), flush=True)
        finally:
            if not ws.closed:
                print("Closing WebSocket: {}".format(ws), flush=True)
                ws.close()
            websocket_list.remove(ws)

    @app.get("set_visual_aid")
    @auth_basic(set_visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_url, websocket_list
        visual_aid_url = request.params["url"]
        if not visual_aid_url.startswith("http"):
            visual_aid_url = "/static/img/visual_aids/" + visual_aid_url
        print("Saved new URL: {!r}".format(visual_aid_url), flush=True)
        # Update WebSockets
        print(websocket_list, flush=True)
        for websocket in websocket_list[:]:
            try:
                print("Sending new URL to {}".format(websocket), flush=True)
                websocket.send(dumps({"url": visual_aid_url}))
            except WebSocketError:
                print("Failed to send message to {}. Removing from list".format(websocket), flush=True)
                websocket_list.remove(websocket)
            except Exception as e:
                print("Error when sending message to {}. {}".format(websocket, e), flush=True)
                websocket_list.remove(websocket)
        if request.params.get("redirect") != "false":
            redirect(visual_aid_url)


def set_visual_aid_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), set_visual_aid_hash)
