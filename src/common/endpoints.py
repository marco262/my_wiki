from json import dumps
from threading import Thread
from time import ctime

import bcrypt
from bottle import static_file, Bottle, view, request, auth_basic
from bottle_websocket import websocket
from git import Repo

from src.common.utils import md_page, websocket_loop, send_to_websockets

START_TIME = ctime()
# Default password: dancinglikeastripper
PLAYER_SOUNDBOARD_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

visual_aid_url = "/static/img/visual_aids/DnD Party 2.png"
websocket_list = []


def init(cfg):
    global GM_NOTES_PW_HASH, PLAYER_SOUNDBOARD_PW_HASH
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")
    PLAYER_SOUNDBOARD_PW_HASH = cfg.get("Password hashes", "Player soundboard").encode("utf-8")


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    def index_help():
        repo = Repo()
        last_commit = repo.head.commit
        commit_history = "{} ({})".format(last_commit.message, ctime(last_commit.committed_date))
        return md_page("home", "common", build_toc=False, commit_history=commit_history, up_to_date_msg=False,
                       last_restart=START_TIME)

    @app.get("/static/<path:path>", name="static")
    def static(path):
        return static_file(path, root="static")

    @app.get("/js/<path:path>", name="js")
    def js(path):
        # # Try to get minified version of JS file first
        # f = static_file(path + ".min", root="js")
        # if isinstance(f, HTTPError) and f.status_code == 404:
        f = static_file(path, root="js")
        return f

    @app.get("/favicon.ico", name="favicon")
    def favicon():
        return static_file("favicon.ico", root="static")

    @app.get('/feedback')
    def feedback():
        return "Feedback here"

    @app.get("/load_changes")
    def restart():
        t = Thread(name="get_git_changes", target=get_git_changes)
        t.start()
        # The bottle server will reload automatically if git updates are found
        return "Checking for git changes..."

    def get_git_changes():
        print("Pulling from git...")
        repo = Repo()
        last_commit = repo.head.commit
        print("HEAD:", last_commit)
        repo.remote().pull()
        new_last_commit = repo.head.commit
        print("New HEAD:", new_last_commit)
        if new_last_commit == last_commit:
            print("No updates found.")
            return "No updates found."
        print("Waiting for server restart")

    @app.get("/restart")
    def restart():
        raise KeyboardInterrupt

    @app.get("/shutdown")
    def shutdown():
        raise SystemExit

    @app.error(404)
    @view("common/page.tpl")
    def error404(error):
        return {"text": "", "title": "404 " + error.body}

    @app.get("/visual_aid")
    @view("common/visual_aid.tpl")
    def visual_aid():
        return

    @app.get('/visual_aid_websocket', apply=[websocket])
    def visual_aid_websocket(ws):
        global visual_aid_url, websocket_list
        ws.send(dumps({"action": "visual_aid", "url": visual_aid_url}))
        websocket_loop(ws, websocket_list)

    @app.post("/set_visual_aid")
    @auth_basic(visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_url
        params = dict(request.params)
        print(params)
        if params["action"] == "visual_aid":
            visual_aid_url = params["url"]
            print("Saved new image URL: {!r}".format(visual_aid_url), flush=True)
        elif params["action"] == "iframe":
            print("Loading iframe with URL: {!r}".format(params["url"]), flush=True)
        else:
            print(f'Sending new {params.get("action")} URL to {params.get("target")}: {repr(params["url"])}', 
                  flush=True)
        if params["debug"] == "true":
            return params["url"]
        else:
            send_to_websockets(params, websocket_list)

    @app.get("/player soundboard")
    def player_soundboard():
        return md_page("Player Soundboard", "common")


def visual_aid_auth_check(username, password):
    return (
        (username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)) or
        (username.lower() == "player" and bcrypt.checkpw(password.encode("utf-8"), PLAYER_SOUNDBOARD_PW_HASH))
    )
