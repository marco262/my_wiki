from glob import glob
from os.path import basename
from re import search

for path in glob("../data/spell/*"):
    print(path)
    with open(path) as f:
        contents = f.read()

    if "title = " in contents:
        continue
    contents = contents.replace("â€™", "'").replace("â€˜", "'").replace("â€”", " -- ")
    # print(contents)
    # print()

    output = ""
    name = basename(path)[:-5].replace('-', ' ').title()
    name = name.replace(" S ", "'s ")
    output += f'title = "{name}"\n'

    classes = [c for c in ["bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard"]
               if f"{c}_spell: {c}_spell" in contents]
    output += "classes = " + str(classes).replace("'", '"') + "\n"

    m = search(r"level: (\d)", contents)
    if m:
        output += f'level = "{m.group(1)}"\n'
    else:
        if "level: cantrip" not in contents:
            raise Exception("No spell level found")
        output += f'level = "cantrip"\n'

    m = search(r"school: (.*?)_school", contents)
    output += f'school = "{m.group(1)}"\n'

    concentration_spell = 'false' if "concentration_spell: '0'" in contents else 'true'
    output += f"concentration_spell = {concentration_spell}\n"

    ritual_spell = 'false' if "ritual_spell: '0'" in contents else 'true'
    output += f"ritual_spell = {ritual_spell}\n"

    m = search(r"casting_time: (.*)", contents)
    casting_time = m.group(1).strip("'")
    output += f'casting_time = "{casting_time}"\n'

    m = search(r"range: (.*)", contents)
    range = m.group(1).strip("'")
    output += f'range = "{range}"\n'

    components = [c[0].upper() for c in ["verbal", "somatic", "material"]
                  if f"{c}_component: {c}_component" in contents]
    output += "components = " + str(components).replace("'", '"') + "\n"

    if "M" in components:
        m = search(r"material_desc: (.*)", contents)
        material = m.group(1).strip("'").replace("'", '"')
        output += f'material = "{material}"\n'

        m = search(r"expensive_material_component: '0'", contents)
        output += f"expensive_material_component = {'false' if m else 'true'}\n"

        m = search(r"material_component_consumed: '0'", contents)
        output += f"material_component_consumed = {'false' if m else 'true'}\n"

    m = search(r"duration: (.*)", contents)
    duration = m.group(1).strip("'")
    output += f'duration = "{duration}"\n'

    m = search(r"description: (.*)", contents)
    description = m.group(1).strip("'").strip('"').replace("''", "'").replace(r"\n", "\n").replace(r"\"", '"')
    description.encode("ascii")
    output += f'description = """{description}"""\n'

    if r"at_higher_levels: at_higher_levels" in contents:
        m = search(r"at_higher_levels_text: (.*)", contents)
        at_higher_levels = m.group(1).strip("'").strip('"').replace("''", "'")
        output += f'at_higher_levels = "{at_higher_levels}"\n'

    d = {
        "phb": "Player's Handbook",
        "dmg": "Dungeon Master's Guide",
        "ee": "Elemental Evil",
        "scag": "Sword Coast Adventurer's Guide",
        "xgte": "Xanathar's Guide to Everything",
        "llok": "Lost Laboratory of Kwalish",
        "homebrew": "Homebrew"
    }
    source = search(r"sourcebook: (.*)", contents).group(1)
    page = search(r"page: '(.*)'", contents).group(1)
    if source == "homebrew":
        output += f'source = "Homebrew"\n'
    else:
        output += f'source = "{d[source]}, p. {page}"\n'

    # print(output)

    with open(path, 'w') as f:
        f.write(output)
    # break
