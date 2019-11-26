from bottle import get, view, static_file, HTTPError


def init():
    pass


def load_wsgi_endpoints():
    @get('/')
    @get('/help')
    @view('home.tpl')
    def index_help():
        return

    @get("/static/:path#.+#", name="static")
    def static(path):
        return static_file(path, root="static")

    @get("/js/:path#.+#", name="js")
    def static(path):
        # Try to get minified version of JS file first
        f = static_file(path + ".min", root="js")
        if isinstance(f, HTTPError) and f.status_code == 404:
            f = static_file(path, root="js")
        return f

    @get('/feedback')
    def feedback():
        return "Feedback here"
