import os
from json import dumps
from threading import Thread
from time import ctime

import bcrypt
from bottle_websocket import websocket
from git import Repo

from bottle import static_file, Bottle, view, request, auth_basic, redirect
from src.common.utils import md_page, websocket_loop, send_to_websockets, track_player_soundboard_clicks, \
    get_player_soundboard_stats

START_TIME = None
# Default password: dancinglikeastripper
PLAYER_SOUNDBOARD_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

visual_aid_type = "visual_aid"
visual_aid_url = "/media/img/visual_aids/arr/arr screen.jpg"
visual_aid_title = "Eorzea welcomes you!"
visual_aid_version = "1.2.2"
websocket_list = []


def init(cfg):
    global START_TIME, GM_NOTES_PW_HASH, PLAYER_SOUNDBOARD_PW_HASH
    START_TIME = ctime()
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")
    PLAYER_SOUNDBOARD_PW_HASH = cfg.get("Password hashes", "Player soundboard").encode("utf-8")


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    def index_help():
        # repo = Repo()
        # last_commit = repo.head.commit
        # commit_history = "{} ({})".format(last_commit.message, ctime(last_commit.committed_date))
        return md_page("home", "common", build_toc=False, commit_history="NULL", up_to_date_msg=False,
                       last_restart=START_TIME)

    @app.get("/static/<path:path>", name="static")
    def static(path):
        return static_file(path, root="static")

    @app.get("/media/<path:path>", name="media")
    def static(path):
        print(os.getenv("RUNNING_IN_DOCKER"))
        if os.getenv("RUNNING_IN_DOCKER") == "True":
            redirect("https://marco262.github.io/my_wiki/media/" + path)
        else:
            return static_file(path, root="media")

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
        ws.send(dumps({
            "action": visual_aid_type, "url": visual_aid_url, "title": visual_aid_title, "version": visual_aid_version
        }))
        websocket_loop(ws, websocket_list)

    @app.post("/set_visual_aid")
    @auth_basic(visual_aid_auth_check)
    def set_visual_aid():
        global visual_aid_type, visual_aid_url, visual_aid_title
        params = dict(request.params)
        print(params)
        if params["action"] == "visual_aid":
            visual_aid_type = "visual_aid"
            visual_aid_url = params["url"]
            visual_aid_title = params["title"]
            print("Saved new image URL: {!r}".format(visual_aid_url), flush=True)
        elif params["action"] == "iframe":
            visual_aid_type = "iframe"
            visual_aid_url = params["url"]
            print("Loading iframe with URL: {!r}".format(visual_aid_url), flush=True)
        else:
            print(
                f'Sending new {params.get("action")} URL to {params.get("target")}: {repr(params["url"])}',
                flush=True
            )
        params["version"] = visual_aid_version
        if params.get("player_soundboard"):
            track_player_soundboard_clicks(params)
        send_to_websockets(params, websocket_list)

    @app.get("/player soundboard")
    def player_soundboard():
        return md_page("Player Soundboard", "common", build_toc=False)

    @app.get("/player soundboard stats")
    @auth_basic(gm_auth_check)
    @view("common/player_soundboard_stats.tpl")
    def player_soundboard_stats():
        stats = get_player_soundboard_stats()
        stats["title"] = "Player Soundboard Stats"
        return stats


def gm_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)


def visual_aid_auth_check(username, password):
    return (
        (username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)) or
        (username.lower() == "player" and bcrypt.checkpw(password.encode("utf-8"), PLAYER_SOUNDBOARD_PW_HASH))
    )
