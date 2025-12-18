import re

from json import load, dumps

from src.common.utils import title_to_page_name

SPELLS_PATH = "../../5etools-src/data/spells/spells-xphb.json"
CLASS_LIST_PATH = "../../5etools-src/data/generated/gendata-spell-source-lookup.json"

with open(SPELLS_PATH) as f:
    spells = load(f)

with open(CLASS_LIST_PATH) as f:
    spell_class_lists = load(f)["xphb"]


def clean_markdown(text: str) -> str:
    text = re.sub(r"{@damage (.*?)}", r"\1", text)
    text = re.sub(r"{@(variantrule|action|condition|status|sense|hazard) (.*?)( \[.*?])?\|XPHB(\|.*?)?}", r"[[glossary:\2]]", text)
    text = re.sub(r"{@item Artisan's Tools\|XPHB}", r"[[[general:equipment#artisans-tools|Artisan's Tools]]]", text)
    text = re.sub(r"{@(skill|item) (.*?)( \[.*?])?\|(XPHB|XDMG)(\|.*?)?}", r"[[tooltip:\2]]", text)
    text = re.sub(r"{@creature (.*?)( \[.*?])?\|.*?}", r"[[[monster:\1]]]", text)
    text = re.sub(r"{@race (.*?)( \[.*?])?\|.*?}", r"[[[advancement:Races#\1]]]", text)
    text = re.sub(r"{@spell (.*?)\|.*?}", r"_[[[spell:\1]]]_", text)
    text = re.sub(r"{@filter (.*?)\|.*?}", r"\1", text)
    text = re.sub(r"{@dice (.*?)}", r"\1", text)
    text = re.sub(r"{@dc (.*?)}", r"DC \1", text)
    text = re.sub(r"{@(scaledamage|scaledice) .*?\|.*?\|(.*?)}", r"\2", text)
    text = re.sub(r"{@chance (.*?)\|.*?}", r"\1 percent chance", text)
    text = re.sub(r"{@book (.*?)\|.*?}", r"\1", text)
    text = re.sub(r"{@b (.*?)}", r"**\1**", text)
    text = re.sub(r"{@i (.*?)}", r"_\1_", text)
    text = text.replace("—", " -- ")
    # Fixes issue where having double quotes in a text field, even when triple-quoted, sometimes breaks parsing.
    text = text.replace(r'"', r'\"')
    # Fix glossary misnomers
    text = text.replace("[[glossary:Opportunity Attack]]", "[[glossary:Opportunity Attacks|Opportunity Attack]]")
    return text


def parse_entries(entries: list[str | dict]) -> str:
    text_list = []
    for e in entries:
        if isinstance(e, str):
            text_list.append(e)
        elif e["type"] == "list":
            inner_list = []
            for item in e["items"]:
                if isinstance(item, str):
                    inner_list.append(" - " + item)
                elif item["type"] == "item":
                    assert len(item["entries"]) == 1
                    inner_list.append(f" - **{item['name']}.** {item['entries'][0]}")
                else:
                    raise ValueError(e)
            text_list.append("\n".join(inner_list))
        elif e["type"] == "entries":
            text_list.append(f"**_{e['name']}._** " + parse_entries(e["entries"]))
        elif e["type"] == "table":
            if "caption" in e:
                text_list.append(f'**{e["caption"]}**')
            text_list.append(make_table(e))
        else:
            raise ValueError(e)
    text = "\n\n".join(text_list)
    return clean_markdown(text)


def make_table(table_data: dict) -> str:
    rows: list = table_data["rows"].copy()
    rows.insert(0, table_data["colLabels"])
    columns = zip(*rows)
    max_lengths = []
    for col in columns:
        max_lengths.append(max(len(s) for s in col))
    lines = []

    def table_row(values: list[str]) -> str:
        cells = []
        for i, cell in enumerate(values):
            cells.append(cell.ljust(max_lengths[i]))
        return "| " + " | ".join(cells) + " |"

    lines.append(table_row(table_data["colLabels"]))
    lines.append("|" + "|".join(["-" * (n + 2) for n in max_lengths]) + "|")
    for row in table_data["rows"]:
        lines.append(table_row(row))
    return "\n".join(lines)


def main():
    for spell in spells["spell"]:
        name = spell["name"]
        print(name)

        source_dict = spell_class_lists[name.lower()]["class"]
        spell_lists = []
        for sourcebook, d in source_dict.items():
            if sourcebook == "TCE":
                continue
            for class_name, b in d.items():
                if b:
                    spell_lists.append(class_name)
        spell_lists.sort()

        match spell["school"]:
            case "A":
                school = "Abjuration"
            case "C":
                school = "Conjuration"
            case "D":
                school = "Divination"
            case "E":
                school = "Enchantment"
            case "V":
                school = "Evocation"
            case "I":
                school = "Illusion"
            case "N":
                school = "Necromancy"
            case "T":
                school = "Transmutation"
            case _:
                raise ValueError(spell["name"], spell["school"])

        assert len(spell["duration"]) == 1
        d = spell["duration"][0]
        if d["type"] == "instant":
            duration = "Instantaneous"
        elif d["type"] == "timed":
            if d["duration"]["amount"] == 1:
                duration = f"1 {d['duration']['type']}"
            else:
                duration = f"{d['duration']['amount']} {d['duration']['type']}s"
        elif d["type"] == "permanent":
            if d["ends"] == ["dispel"]:
                duration = "Until dispelled"
            elif d["ends"] == ["dispel", "trigger"]:
                duration = "Until dispelled or triggered"
            else:
                raise ValueError(d)
        elif d["type"] == "special":
            duration = "Special"
        else:
            raise ValueError(d)
        concentration = "true" if d.get("concentration") else "false"

        ritual = spell.get("meta", {}).get("ritual")
        ritual = "true" if ritual else "false"

        time_entries = []
        for t in spell["time"]:
            if t["unit"] == "action":
                text = "Action"
            elif t["unit"] == "bonus":
                text = "Bonus Action"
            elif t["unit"] == "reaction":
                text = f"Reaction"
            else:
                text = f"{t['number']} {t['unit']}"
            if t.get("condition"):
                text += ", " + t["condition"]
            if "note" in t:
                text += f' ({t["note"]})'
            time_entries.append(text)
        casting_time = " or ".join(time_entries)
        casting_time = clean_markdown(casting_time)

        r = spell["range"]
        if r["type"] == "point":
            if r["distance"]["type"] in ("self", "touch", "sight", "unlimited"):
                range = r["distance"]["type"].title()
            else:
                range = f'{r["distance"]["amount"]} {r["distance"]["type"]}'
        elif r["type"] in ("cone", "cube", "emanation", "line", "sphere"):
            unit = r["distance"]["type"]
            if unit == "feet":
                unit = "foot"
            elif unit == "miles":
                unit = "mile"
            else:
                raise ValueError(unit)
            range = f'Self ({r["distance"]["amount"]}-{unit} [[glossary:{r["type"]}]])'
        else:
            raise ValueError(r)

        components = [k.upper() for k in spell["components"].keys()]

        output = f"""title = "{name}"
spell_lists = {dumps(spell_lists)}
level = "{spell["level"]}"
school = "{school}"
concentration_spell = {concentration}
ritual_spell = {ritual}
casting_time = "{casting_time}"
range = "{range}"
components = {dumps(components)}
"""

        if "m" in spell["components"]:
            m = spell["components"]["m"]
            if isinstance(m, str):
                expensive = "false"
                cost = 0
                consumed = "false"
            else:
                expensive = "true" if m.get("cost") else "false"
                cost = m.get("cost", 0)
                consumed = "true" if m.get("consume") else "false"
                m = m["text"]
            m = clean_markdown(m)
            output += f"""material = "{m}"
expensive_material_component = {expensive}
material_component_cost = {cost}
material_component_consumed = {consumed}
"""

        output += f'duration = "{duration}"\n'

        desc = parse_entries(spell["entries"])
        if len(spell["entries"]) == 1:
            output += f'description = "{desc}"\n'
        else:
            output += f'description = """\n{desc}\n"""\n'

        if "entriesHigherLevel" in spell:
            assert len(spell["entriesHigherLevel"]) == 1
            e = spell["entriesHigherLevel"][0]
            text = parse_entries(e["entries"])
            if spell["level"] == 0:
                output += f'cantrip_upgrade = "{text}"\n'
            else:
                output += f'at_higher_levels = "{text}"\n'

        output += f'source = "Player\'s Handbook, p. {spell["page"]}"\n'

        with open(f"../data/dnd/spell/{title_to_page_name(name)}.toml", "w") as f:
            f.write(output)


if __name__ == '__main__':
    main()
