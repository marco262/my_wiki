import os
import sys
import tempfile
import threading
from json import dumps, load, dump, loads
from threading import Thread
from time import ctime
from typing import Optional
from urllib.parse import urljoin

import bcrypt
from bottle import static_file, Bottle, view, request, auth_basic, redirect
from bottle_websocket import websocket
from git import Repo

import src.common.utils as utils
from src.common.markdown_parser import DEFAULT_MARKDOWN_PARSER
from src.common.utils import md_page, websocket_loop, send_to_websockets, track_player_soundboard_clicks, \
    get_player_soundboard_stats, check_for_media_file, save_media_file

START_TIME = None
# Default password: dancinglikeastripper
PLAYER_SOUNDBOARD_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"
GM_NOTES_PW_HASH = b"$2b$12$CQk/8o5DPPy05njxM8kO4e/WWr5UV7EXtE1sjctnKAUCLj5nqTcHC"

visual_aid_type = "visual_aid"
visual_aid_url = "/media/img/visual_aids/arr/ARR Opening Wallpaper.png"
visual_aid_title = "The Nerds of Light"
visual_aid_version = "1.3.0"
volume_settings: Optional[dict] = None
websocket_list = []

# Create a mutex lock
volume_control_lock = threading.Lock()


def init(cfg):
    global START_TIME, GM_NOTES_PW_HASH, PLAYER_SOUNDBOARD_PW_HASH, volume_settings
    START_TIME = ctime()
    GM_NOTES_PW_HASH = cfg.get("Password hashes", "GM Notes").encode("utf-8")
    PLAYER_SOUNDBOARD_PW_HASH = cfg.get("Password hashes", "Player soundboard").encode("utf-8")
    if os.path.isfile("volume_settings.json"):
        with open("volume_settings.json") as f:
            volume_settings = load(f)
    else:
        volume_settings = {"music": 1.0, "ambience": 1.0, "effect": 1.0}
    utils.MEDIA_BUCKET = cfg.get("Settings", "media bucket")


def save_volume_settings(params: dict):
    global volume_settings
    volume_settings = params
    with open("volume_settings.json", "w") as f:
        dump(volume_settings, f)


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

    @app.get("/media/<path:path>", name="media")
    def media(path):
        if utils.MEDIA_BUCKET:
            redirect(urljoin(f"https://storage.googleapis.com/{utils.MEDIA_BUCKET}/media/", path))
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
        print("Checking GitHub for any changes...")
        repo = Repo()
        last_commit = repo.head.commit
        print("HEAD:", last_commit)
        remote = repo.remote()
        print("Stashing any existing changes")
        repo.git.stash("save")
        print("Pulling from GitHub")
        remote.pull()
        remote_last_commit = remote.repo.head.commit
        print("Remote HEAD:", remote_last_commit)
        print("Applying any stashed changes")
        repo.git.stash("push")
        if remote_last_commit == last_commit:
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
        return {"volume_settings": dumps(volume_settings)}

    @app.get('/visual_aid_websocket', apply=[websocket])
    def visual_aid_websocket(ws):
        global visual_aid_url, websocket_list
        print(dict(request.headers))
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
        if "action" not in params:
            # Try to handle weird Obsidian params packing
            params = loads(list(params.keys())[0])
        if params["action"] == "visual_aid":
            visual_aid_type = "visual_aid"
            visual_aid_url = params["url"]
            # Parse the title with Markdown
            params["title"] = DEFAULT_MARKDOWN_PARSER.parse_md(params["title"])
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

    @app.post("/check_visual_aid")
    @auth_basic(visual_aid_auth_check)
    def check_visual_aid():
        body = loads(request.body.getvalue())
        path = f"media/img/visual_aids/{body['target_path']}"
        print(path)
        expected_file_size = int(body["image_size"])
        return {"size_matches": check_for_media_file(path, file_size=expected_file_size)}

    @app.put("/upload_visual_aid")
    @auth_basic(visual_aid_auth_check)
    def upload_visual_aid():
        """
        The request body must be a bytes string, where the first line (up to \n) is a JSON dict with a
        `target_path` field representing the path to save the file to.
        """
        temp_file: tempfile._TemporaryFileWrapper = request.body
        metadata = loads(temp_file.readline().decode("utf-8").strip("\n"))
        path = f"media/img/visual_aids/{metadata['target_path']}"
        print(path)
        save_media_file(path, temp_file.read())
        temp_file.close()

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

    @app.get("/get_volume_settings")
    def soundboard_volume_settings():
        return volume_settings

    @app.post("/set_volume")
    @auth_basic(visual_aid_auth_check)
    def set_soundboard_volume():
        params = dict(request.params)
        err_msg = f"{params} is not a valid volume setting"
        for k, v in params.items():
            if k not in ("music", "ambience", "effect"):
                print(err_msg, file=sys.stderr)
                break
            try:
                value = float(v)
            except ValueError:
                print(err_msg, file=sys.stderr)
                break
            else:
                if 0 <= value <= 1:
                    params[k] = value
                else:
                    print(err_msg, file=sys.stderr)
                    break
        else:
            print(params)
            save_volume_settings(params)
            send_to_websockets(
                {"version": visual_aid_version, "action": "volume", "settings": params},
                websocket_list
            )
        return params


def gm_auth_check(username, password):
    return username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)


def visual_aid_auth_check(username, password):
    return (
        (username.lower() == "gm" and bcrypt.checkpw(password.encode("utf-8"), GM_NOTES_PW_HASH)) or
        (username.lower() == "player" and bcrypt.checkpw(password.encode("utf-8"), PLAYER_SOUNDBOARD_PW_HASH))
    )
