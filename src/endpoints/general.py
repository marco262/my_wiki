from bottle import view, static_file, HTTPError, Bottle


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get('/')
    @app.get('/help')
    @view('home.tpl')
    def index_help():
        return

    @app.get("/static/:path#.+#", name="static")
    def static(path):
        return static_file(path, root="static")

    @app.get("/js/:path#.+#", name="js")
    def js(path):
        # Try to get minified version of JS file first
        f = static_file(path + ".min", root="js")
        if isinstance(f, HTTPError) and f.status_code == 404:
            f = static_file(path, root="js")
        return f

    @app.get("/favicon.ico", name="favicon")
    def favicon():
        return static_file("favicon.ico", root="static")

    @app.get('/feedback')
    def feedback():
        return "Feedback here"
