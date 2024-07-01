from bottle import HTTPError, Bottle

from data.dnd.enums import spell_classes
from src.common import utils
from src.common.utils import title_to_page_name
from src.dnd.utils import load_spells


def load_api_endpoints(app: Bottle):
    @app.get("/hello")
    def hello():
        return {"message": "Hello World!"}

    # @app.get("/<path:path>")
    # def get_dnd_api():
    #     return {"message": f"Hello {path}"}

# def api(path: str):
#     type_, path = utils.splitter(path, "/", 2)
#     if type_ == "spell_list":
#         name, level = utils.splitter(path, "/", 2)
#         name = name.lower()
#         spells = load_spells()
#         if name in ("", "all"):
#             return spells
#         # Get spell lists by class
#         if name not in spell_classes:
#             raise HTTPError(404, f'"{name}" is not a valid spell list.')
#         d = {k: v for k, v in spells.items() if name in v["classes"]}
#         # If no level, return list
#         if level == "":
#             return d
#         level = level.lower()
#         # Filter more by level
#         if not (level == "cantrip" or (level.isdigit() and 0 <= int(level) <= 9)):
#             raise HTTPError(404, f'"{level}" is not a valid spell level.')
#         if level == "0":
#             level = "cantrip"
#         return {k: v for k, v in d.items() if level == v["level"]}
#     elif type_ == "spell":
#         formatted_name = title_to_page_name(path)
#         spells = load_spells()
#         if formatted_name not in spells:
#             raise HTTPError(404, f"I couldn't find a spell by the name of \"{path}\".")
#         return spells[formatted_name]
#     else:
#         raise HTTPError(404, f"Unknown API type: \"{type_}\"")