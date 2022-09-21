from glob import glob
from json import dumps, loads

import bcrypt
import os
import random
from bottle_websocket import websocket

from bottle import Bottle, view, auth_basic, request
from data.curse_of_strahd.enums import tarokka_deck
from src.common.utils import md_page, websocket_loop, send_to_websockets

# Default password: dancinglikeastripper
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

websocket_list = []
TAROKKA_CARD_LIST = None
last_tarokka_setup = {
    "top": {"card": "6 of Glyphs - Anarchist", "inverted": True},
    "left": {"card": "Master of Coins - Rogue", "inverted": False},
    "middle": {"card": "High Deck - Temptress", "inverted": True},
    "right": {"card": "4 of Glyphs - Shepherd", "inverted": True},
    "bottom": {"card": "9 of Glyphs - Traitor", "inverted": False}
}


def init(cfg):
    global GM_NOTES_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")


def get_tarokka_card_list():
    global TAROKKA_CARD_LIST
    if TAROKKA_CARD_LIST is not None:
        return TAROKKA_CARD_LIST
    TAROKKA_CARD_LIST = []
    for filepath in glob("media/img/tarokka/*"):
        filename = os.path.basename(filepath)
        if not filename.endswith(".png"):
            continue
        if filename == "__Back.png" or filename == "High Deck - Tempter.png":
            continue
        TAROKKA_CARD_LIST.append(os.path.splitext(filename)[0])
    return TAROKKA_CARD_LIST


def create_random_reading(forced_cards):
    chosen_cards = random.sample(get_tarokka_card_list(), 5)
    reading = {}
    for position in ["top", "left", "middle", "right", "bottom"]:
        if position in forced_cards:
            reading[position] = forced_cards[position]
            forced_card = forced_cards[position]["card"]
            if forced_card in chosen_cards:
                chosen_cards.remove(forced_card)
        else:
            reading[position] = {
                "card": chosen_cards.pop(),
                "inverted": random.choice([True, False])
            }
    return reading


def alter_tarokka_list(key, payload):
    global last_tarokka_setup
    data = loads(payload["data"])
    if data["position"] == "all":
        for d in last_tarokka_setup.values():
            d[key] = data["state"]
    else:
        last_tarokka_setup[data["position"]][key] = data["state"]


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("Curse of Strahd", "curse_of_strahd")

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        return md_page(name, "curse_of_strahd")

    @app.get("")
    @view("common/page.tpl")
    def calendar():
        return md_page("calendar", "curse_of_strahd", build_toc=False)

    @app.get("tarokka")
    @view("curse_of_strahd/tarokka.tpl")
    def tarokka():
        return

    @app.get("tarokka_card_list")
    @view("curse_of_strahd/tarokka_card_list.tpl")
    def tarokka_card_list():
        return {"title": "Tarokka Card List", "tarokka_deck": tarokka_deck}

    @app.get("/tarokka_websocket", apply=[websocket])
    def tarokka_websocket(ws):
        global websocket_list
        ws.send(dumps({"action": "sync", "data": dumps(last_tarokka_setup)}))
        websocket_loop(ws, websocket_list)

    @app.post("/play_tarokka")
    def play_tarokka():
        global last_tarokka_setup
        payload = dict(request.params)
        if payload["action"] == "set_random_reading":
            last_tarokka_setup = create_random_reading(loads(payload["data"]))
            payload = {"action": "set", "data": dumps(last_tarokka_setup)}
        elif payload["action"] == "set_from_file":
            with open(f"data/curse_of_strahd/gm_notes/tarroka_readings/{payload['data']}.json") as f:
                data = f.read().strip("\n")
            last_tarokka_setup = loads(data)
            payload = {"action": "set", "data": data}
        elif payload["action"] == "force_cards":
            data = loads(payload["data"])
            for position, card_dict in data.items():
                last_tarokka_setup[position] = card_dict
            payload = {"action": "sync", "data": dumps(last_tarokka_setup)}
        elif payload["action"] == "invert":
            alter_tarokka_list("inverted", payload)
            payload = {"action": "sync", "data": dumps(last_tarokka_setup)}
        elif payload["action"] == "deal":
            alter_tarokka_list("off-grid", payload)
        elif payload["action"] == "flip":
            alter_tarokka_list("flipped", payload)
        elif payload["action"] == "reset":
            for d in last_tarokka_setup.values():
                d["off-grid"] = True
                d["flipped"] = False
        elif payload["action"] == "sync":
            payload["data"] = dumps(last_tarokka_setup)
        if payload["action"] != "get_sync_data":
            send_to_websockets(payload, websocket_list)
        return last_tarokka_setup

    @app.get("gm_notes/Tarokka Controls")
    @view("curse_of_strahd/tarokka_controls.tpl")
    def tarokka_controls():
        return

    @app.get("gm_notes/<name>")
    @view("common/page.tpl")
    @auth_basic(gm_notes_auth_check)
    def gm_notes(name):
        return md_page(name, "curse_of_strahd", directory="gm_notes")


def gm_notes_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)
