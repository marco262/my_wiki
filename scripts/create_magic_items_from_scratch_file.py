import glob
import os
import re

from src.common.utils import title_to_page_name

BASE_DIR = "../data/dnd/equipment/magic-items"
NEW_DIR = os.path.join(BASE_DIR, "new")

# os.makedirs(NEW_DIR, exist_ok=True)
# 
# with open(os.path.join(BASE_DIR, "scratch.md"), "rb") as f:
#     file_contents = f.read().decode("utf-8").replace("\r", "")
# 
# for item in file_contents.split("----"):
#     lines = item.strip("\n")
#     first_line = lines.split("\n")[0]
#     print(first_line)
#     if not first_line:
#         print(repr(lines))
#         break
#     page_name = title_to_page_name(first_line)
#     print(page_name)
#     with open(os.path.join(NEW_DIR, page_name + ".md"), 'wb') as f:
#         f.write(lines.encode("utf-8"))

for filepath in glob.glob(os.path.join(NEW_DIR, "*.md")):
    with open(filepath, "rb") as f:
        file_contents = f.read().decode("utf-8").replace("\r", "")
    name, stats, _, description = file_contents.split("\n", 3)

    if m := re.match(r"Wondrous item( \((.*?)\))?", stats):
        item_type = "Wondrous Item"
        subtype = m.group(2)
    elif m := re.match(r"Weapon( \((.*?)\))?", stats):
        item_type = "Weapon"
        subtype = m.group(2)
    else:
        raise ValueError(stats)
    subtype = subtype if subtype else ""

    if "uncommon" in stats:
        rarity = "Uncommon"
    elif "common" in stats:
        rarity = "Common"
    elif "very rare" in stats:
        rarity = "Very Rare"
    elif "rare" in stats:
        rarity = "Rare"
    elif "legendary" in stats:
        rarity = "Legendary"
    elif "artifact" in stats:
        rarity = "Artifact"
    else:
        raise ValueError(stats)

    attunement = str("requires attunement" in stats).lower()

    if m := re.search(r"\(requires attunement by an? (.*?)\)", stats):
        classes = [c.lower() for c in m.group(1).split(" or ")]
    else:
        classes = []
    classes = str(classes).replace("'", '"')
    
    description = description.strip("\n")

    toml_contents = f'''title = "{name}"
type = "{item_type}"
subtype = "{subtype}"
rarity = "{rarity}"
attunement = {attunement}
classes = {classes}
notes = ""
source = "tcoe "
description = """
{description}
"""
'''
    with open(filepath.replace(".md", ".toml"), 'wb') as f:
        f.write(toml_contents.encode("utf-8"))
