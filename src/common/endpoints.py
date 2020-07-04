from git import Repo
from time import ctime

from bottle import static_file, Bottle
from src.common.utils import md_page

START_TIME = ctime()


def init():
    pass


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
        # The bottle server will reload automatically
        return "Restarting"
