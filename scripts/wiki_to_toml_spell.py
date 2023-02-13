import re
from glob import glob
from json import dumps
from os.path import basename
from re import search


source = "Cleric and Revised Species"

for path in glob("../data/onednd/spell/*"):
    print(path)
    with open(path) as f:
        contents = f.read()

    if "title = " in contents:
        continue

    contents = re.sub(r"’", "'", contents)
    contents = re.sub(r"“", '"', contents)
    contents = re.sub(r"”", '"', contents)
    contents = re.sub(r" ?— ?", " -- ", contents)
    print(contents)
    # print()

    print(r"(?P<name>.*?)\n"
        r"(?P<level>\d)(\w\w)?-Level (?P<school>.*?) Spell \((?P<spell_lists>.*?)\)\n"
        r"Casting Time: (?P<casting_time>.*?)\n"
        r"Range: (?P<range>.*?)\n"
        r"Components: (?P<components>.*?)( \((?P<material>.*?)\))?\n"
        r"Duration: (?P<duration>.*?)\n"
        r"(?P<description>.*)")

    m = re.match(
        r"(?P<name>.*?)\n"
        r"(?P<level>\d)(\w\w)?-Level (?P<school>.*?) Spell \((?P<spell_lists>.*?)\)\n"
        r"Casting Time: (?P<casting_time>.*?)\n"
        r"Range: (?P<range>.*?)\n"
        r"Components: (?P<components>.*?)( \((?P<material>.*?)\))?\n"
        r"Duration: (?P<duration>.*?)\n"
        r"(?P<description>.*)",
        contents,
        flags=re.DOTALL
    )
    print(m.groups())

    output = ""

    name = m["name"].replace(" ", "").title()
    output += f'title = "{name}"\n'

    spell_lists = m['spell_lists'].split(", ")
    output += f"spell_lists = {dumps(spell_lists)}\n"

    output += f'level = "{m["level"]}"\n'

    output += f'school = "{m["school"]}"\n'

    concentration_spell = "true" if "Concentration" in m["duration"] else "false"
    output += f"concentration_spell = {concentration_spell}\n"

    output += "ritual_spell = false\n"

    casting_time = m["casting_time"].replace("\n", " ").strip(" ")
    output += f'casting_time = "{casting_time}"\n'

    output += f'range = "{m["range"]}"\n'

    components = m['components'].split(", ")
    output += f"components = {dumps(components)}\n"

    if "M" in components:
        material = m["material"].replace("\n", " ").strip(" ")
        output += f'material = "{material}"\n'

        output += f"expensive_material_component = {'true' if 'gp' in m['material'] else 'false'}\n"

        output += f"material_component_consumed = {'true' if 'consumed' in m['material'] else 'false'}\n"

    if "Concentration" in m["duration"]:
        duration = re.match(r"Concentration, up to (.*)", m["duration"]).group(1)
    else:
        duration = m["duration"]
    output += f'duration = "{duration}"\n'

    if "At Higher Levels." in m["description"]:
        m2 = re.match(r"(.*?)At Higher Levels. (.*)", m["description"], flags=re.DOTALL)
        description = m2.group(1)
        at_higher_levels = m2.group(2)
    else:
        description = m["description"]
        at_higher_levels = None

    description = description.replace("\n", " ").strip(" ").replace("@", "  ")
    output += f'description = """{description}"""\n'

    if at_higher_levels:
        at_higher_levels = at_higher_levels.replace("\n", " ").strip(" ")
        output += f'at_higher_levels = "{at_higher_levels}"\n'

    output += f'source = "{source}"\n'

    print(output)

    with open(path, 'w') as f:
        f.write(output)
    # break
    print("-----------------")
