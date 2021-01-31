from glob import glob
from json import dumps

import bcrypt
import os
import random
from bottle_websocket import websocket

from bottle import Bottle, view, auth_basic, request
from src.common.utils import md_page, websocket_loop, send_to_websockets

# Default password: dancinglikeastripper
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

websocket_list = []
TAROKKA_CARD_LIST = None
last_tarokka_setup = '{"top": {"card": "6 of Glyphs - Anarchist", "inverted": true}, "left": {"card": "Master of Coins - Rogue", "inverted": false}, "middle": {"card": "High Deck - Temptress", "inverted": true}, "right": {"card": "4 of Glyphs - Shepherd", "inverted": true}, "bottom": {"card": "9 of Glyphs - Traitor", "inverted": false}}'


def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")


def get_tarokka_card_list():
    global TAROKKA_CARD_LIST
    if TAROKKA_CARD_LIST is not None:
        return TAROKKA_CARD_LIST
    TAROKKA_CARD_LIST = []
    for filepath in glob("static/img/tarokka/*"):
        filename = os.path.basename(filepath)
        if not filename.endswith(".png"):
            continue
        if filename == "__Back.png" or filename == "High Deck - Tempter.png":
            continue
        TAROKKA_CARD_LIST.append(os.path.splitext(filename)[0])
    return TAROKKA_CARD_LIST


def create_random_reading():
    chosen_cards = random.sample(get_tarokka_card_list(), 5)
    return {
        "top": {
            "card": chosen_cards[0],
            "inverted": random.choice([True, False])
        },
        "left": {
            "card": chosen_cards[1],
            "inverted": random.choice([True, False])
        },
        "middle": {
            "card": chosen_cards[2],
            "inverted": random.choice([True, False])
        },
        "right": {
            "card": chosen_cards[3],
            "inverted": random.choice([True, False])
        },
        "bottom": {
            "card": chosen_cards[4],
            "inverted": random.choice([True, False])
        },
    }


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
    def tarokka():
        return

    @app.get("/tarokka_websocket", apply=[websocket])
    def tarokka_websocket(ws):
        global websocket_list
        ws.send(dumps({"action": "set", "data": last_tarokka_setup}))
        websocket_loop(ws, websocket_list)

    @app.post("/play_tarokka")
    @auth_basic(gm_notes_auth_check)
    def play_tarokka():
        global last_tarokka_setup
        payload = dict(request.params)
        if payload["action"] == "set_random_reading":
            payload = {"action": "set", "data": dumps(create_random_reading())}
        elif payload["action"] == "set_from_file":
            with open(f"data/curse_of_strahd/gm_notes/tarroka_readings/{payload['data']}.json") as f:
                payload = {"action": "set", "data": f.read().strip("\n")}
        # Save last tarokka setup
        if payload["action"] == "set":
            last_tarokka_setup = payload["data"]
        send_to_websockets(payload, websocket_list)


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
