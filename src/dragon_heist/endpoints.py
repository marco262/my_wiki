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


def websocket_loop(ws, websocket_list):
    print("Opening Websocket {}".format(ws), flush=True)
    websocket_list.append(ws)
    try:
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
        try:
            websocket_list.remove(ws)
        except ValueError as e:
            print(e, ws)


def send_to_websockets(payload):
    global websocket_list
    print(websocket_list, flush=True)
    for ws in websocket_list[:]:
        try:
            print(f"Sending payload {payload} to {ws}", flush=True)
            ws.send(dumps(payload))
        except WebSocketError:
            print(f"Failed to send message to {ws}. Removing from list", flush=True)
            websocket_list.remove(ws)
        except Exception as e:
            print(f"Error when sending message to {ws}. {e}", flush=True)
            websocket_list.remove(ws)


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

    @app.get('/visual_aid_websocket', apply=[websocket])
    def visual_aid_websocket(ws):
        global visual_aid_url, websocket_list
        ws.send(dumps({"target": "visual_aid", "url": visual_aid_url}))
        websocket_loop(ws, websocket_list)

    @app.post("set_visual_aid")
    @auth_basic(set_visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_url
        params = dict(request.params)
        print(params)
        url = params.get("url")
        if params["action"] == "visual_aid":
            if url and not url.startswith("http"):
                url = "/static/img/visual_aids/" + url
            visual_aid_url = request.params["url"]
            print("Saved new image URL: {!r}".format(visual_aid_url), flush=True)
        else:
            if url and not url.startswith("http"):
                url = "/static/audio/" + url
            print(f'Sending new {params.get("action")} URL to {params.get("target")}: {repr(url)}', flush=True)
        params["url"] = url
        if params["debug"] == "true":
            return url
        else:
            send_to_websockets(params)


def set_visual_aid_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), set_visual_aid_hash)
