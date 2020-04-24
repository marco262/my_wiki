import sys

from git import Repo
from time import ctime

from bottle import static_file, Bottle, redirect, view
from src.common.utils import md_page


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    def index_help():
        repo = Repo()
        last_commit = repo.active_branch.log()[-1]
        commit_history = "{} ({})".format(last_commit.message, ctime(last_commit.time[0]))
        return md_page("home", "common", build_toc=False, commit_history=commit_history)

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
    @view("common/load_changes")
    def restart():
        print("Pulling from git...", end="")
        repo = Repo()
        repo.remote().pull()
        print(" Done.")
        print("Waiting for server restart")
        # The bottle server will reload automatically
