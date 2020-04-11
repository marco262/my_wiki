from json import dumps

from bottle import Bottle, view, request, response

from src.common.utils import md_page

visual_aid_url = ""


def init():
    pass


def load_wsgi_endpoints(app: Bottle):
    @app.get("/")
    @app.get("/home")
    def home():
        return md_page("home", "dragon_heist")

    @app.get("")
    @view("common/page.tpl")
    def calendar():
        return md_page("calendar", "dragon_heist", build_toc=False)

    @app.get("<name>")
    @view("common/page.tpl")
    def page(name):
        print("Fuck this shit")
        return md_page(name, "dragon_heist")

    @app.get("visual_aid")
    @view("common/page.tpl")
    def visual_aid():
        return md_page("visual_aid", "dragon_heist")

    @app.get("get_visual_aid")
    def get_visual_aid():
        global visual_aid_url
        url = request.params["visual_aid_url"]
        response.content_type = 'application/json'
        return dumps({"url": url})

    @app.post("set_visual_aid")
    def set_visual_aid():
        global visual_aid_url
        visual_aid_url = request.params["visual_aid_url"]
