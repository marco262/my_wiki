from bottle import static_file, HTTPError, Bottle
from src.common.utils import md_page


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    def index_help():
        return md_page("home", "", build_toc=False)

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
