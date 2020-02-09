from bottle import Bottle, view, request

from data.numenera import enums
from src.markdown_parser import MarkdownParser
from src.numenera_utils import pick_two_mutations, pick_mutation
from src.utils import create_tooltip, md_page

MD = None


def init():
    global MD
    MD = MarkdownParser()


def load_wsgi_endpoints(app: Bottle):

    @app.get("/numenera")
    @view("numenera/page.tpl")
    def home():
        md = MD.parse_md_path("data/numenera/home.md")
        return {"title": "Numenera", "text": md, "toc": md.toc_html}

    @app.get("/numenera/Mutations Generator")
    @view("numenera/mutations_generator.tpl")
    def mutations_generator():
        return

    @app.post("/numenera/mutations_generator_results")
    def mutations_generator_results():
        selected_option = request.params["selected"]
        if selected_option == "2 Beneficial":
            mutation_lists = ["beneficial", "beneficial"]
        elif selected_option == "3 Beneficial and 1 Harmful":
            mutation_lists = ["beneficial", "beneficial", "beneficial", "harmful"]
        elif selected_option == "1 Powerful and 1 Harmful":
            mutation_lists = ["powerful", "harmful"]
        elif selected_option == "1 Powerful, 1 Distinctive, 1 Harmful":
            mutation_lists = ["powerful", "distinctive", "harmful"]
        else:
            raise ValueError("FARTS lol farts {}".format(selected_option))
        mutation_lists += ["cosmetic", "cosmetic", "cosmetic", "cosmetic"]
        output = '<div class="no-border">\n'
        output += '<table class="no-border" style="margin-left: 1em">\n'
        output += '<style>td {padding-left: 1em; padding-right: 1em;}</style>'
        for mutation_list_name in mutation_lists:
            output += "<tr>"
            m1, m2 = pick_two_mutations(getattr(enums, mutation_list_name + "_mutations"))
            m1_tt = create_tooltip(m1[2], m1[3] if len(m1) > 3 else None)
            m2_tt = create_tooltip(m2[2], m2[3] if len(m2) > 3 else None)
            output += f"    <td><em>{mutation_list_name.title()}</em></td>\n" \
                      f"    <td>{m1_tt}</td>\n" \
                      f"    <td>OR</td>\n" \
                      f"    <td>{m2_tt}</td>\n" \
                      f"</tr>\n"
        output += "</table>\n"
        output += "</div>\n"
        output += "<br>\nIf a mutation above gives you an extra beneficial mutation, you also get:<br><br>\n"
        m = pick_mutation(enums.beneficial_mutations)
        output += "&nbsp;&nbsp;&nbsp;&nbsp;" + create_tooltip(m[2], m[3])
        return output

    @app.get('/numenera/<name>')
    @view("numenera/page.tpl")
    def page(name):
        return md_page(name, "numenera", MD)
