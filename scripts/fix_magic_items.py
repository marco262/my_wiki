import glob
import os
import re

from data.dnd.enums import classes
from src.common.utils import title_to_page_name
from src.dnd.endpoints import load_spells

os.chdir("..")
BASE_DIR = "data/dnd/equipment/magic-items"

# spells = load_spells()
# 
# spell_names = [s["title"].lower() for s in spells.values()]
# spell_names.remove("dawn")
# spell_names.remove("resistance")
# spell_names.remove("symbol")
# spell_names.remove("shield")
# spell_names.remove("command")
# spell_names.remove("light")
# spell_names.remove("fall")

for filepath in glob.glob(os.path.join(BASE_DIR, "*.toml")):
    with open(filepath, "rb") as f:
        old_file_contents = f.read().decode("utf-8").replace("\r", "")

    file_contents = old_file_contents

    # if "subtype = " not in file_contents:
    #     file_contents = re.sub(r"type = (.*)", r'type = \1\nsubtype = ""', file_contents)
    # 
    # if "classes = " not in file_contents:
    #     file_contents = re.sub(r"attunement = (.*)", r'attunement = \1\nclasses = []', file_contents)

    # if (m := re.search(r'notes = "(.+?)"', file_contents)):
    #     file_contents = file_contents.replace(m.group(0), 'notes = ""')
    #     if m.group(1) in classes:
    #         file_contents = file_contents.replace('classes = []', f'classes = ["{m.group(1)}"]')
    #     else:
    #         file_contents = file_contents.replace('subtype = ""', f'subtype = "{m.group(1)}"')

    # if "comprehend" in filepath:
    #     print("")
    # 
    # if "spell" in file_contents:
    #     for s in spell_names:
    #         file_contents = re.sub(f"\\b{s}\\b", f"_[[[spell:{s}]]]_", file_contents)

    if "rarity_type =" not in file_contents:
        m = re.search(r'rarity = "(.*?)"\nattunement = (.*?)\n', file_contents)
        if m.group(1) == "Common" or m.group(2) == "false":
            rarity_type = "Minor"
        else:
            rarity_type = "Major"
        file_contents = file_contents.replace(
            m.group(0),
            f'rarity_type = "{rarity_type}"\nrarity = "{m.group(1)}"\nattunement = {m.group(2)}\n'
        )

    if file_contents != old_file_contents:
        print(filepath)
        with open(filepath, 'wb') as f:
            f.write(file_contents.encode("utf-8"))
