from json import load

from src.common.utils import title_to_page_name, ordinal

cr_to_xp = {
    "0": "10",
    "1/8": "25",
    "1/4": "50",
    "1/2": "100",
    "1": "200",
    "2": "450",
    "3": "700",
    "4": "1,100",
    "5": "1,800",
    "6": "2,300",
    "7": "2,900",
    "8": "3,900",
    "9": "5,000",
    "10": "5,900",
    "11": "7,200",
    "12": "8,400",
    "13": "10,000",
    "14": "11,500",
    "15": "13,000",
    "16": "15,000",
    "17": "18,000",
    "18": "20,000",
    "19": "22,000",
    "20": "25,000",
    "21": "33,000",
    "22": "41,000",
    "23": "50,000",
    "24": "62,000",
    "25": "75,000",
    "26": "90,000",
    "27": "105,000",
    "28": "120,000",
    "29": "135,000",
    "30": "155,000"
}


def dict_to_stats(d):
    return ", ".join([f"{stat.title()} {score}" for stat, score in d.items()])


def handle_resistances(resistances, r_type="resist"):
    resistances_list = []
    delimiter = ", "
    for r in resistances:
        if isinstance(r, str):
            r_string = r
        elif "special" in r:
            r_string = r["special"]
        elif r_type in r:
            delimiter = "; "
            r_string = ", ".join(r[r_type])
            if "preNote" in r:
                r_string = f"{r['preNote']} {r_string}"
            if "note" in r:
                r_string += f" {r['note']}"
            r_string = r_string
        else:
            raise ValueError(r)
        if r_type == "conditionImmune":
            r_string = "{@condition %s}" % r_string
        resistances_list.append(r_string)
    return delimiter.join(resistances_list)


def handle_entries(output, name, entries):
    output.append(f'***{name}.*** {entries[0]}')
    for line in entries[1:]:
        output.append("")
        if isinstance(line, dict):
            for item in line["items"]:
                if item.get("style") == "italic":
                    header = f"_{item['name']}_"
                else:
                    header = f"**{item['name']}**"
                if "entry" in item:
                    output.append(f"{header} {item['entry']}  ")
                elif "entries" in item:
                    output.append(f"{header} {item['entries'][0]}  ")
                    for entry in item["entries"][1:]:
                        output.append(f"{entry}  ")
        else:
            output.append(line)


def handle_cr(cr):
    return f"{cr} ({cr_to_xp[cr]} XP)"


def add_actions_and_stuff(output, monster, key, name):
    if key in monster:
        output.append(f'{name} = """!')
        if key == "legendary":
            output.append(
                f"The {monster['name']} can take 3 legendary actions, choosing from the options below. Only one "
                f"legendary action option can be used at a time and only at the end of another creature's turn. "
                f"The {monster['name']} regains spent legendary actions at the start of its turn."
            )
            output.append("")
        for i, d in enumerate(monster[key]):
            if i > 0:
                output.append("")
            handle_entries(output, d["name"], d["entries"])
        output.append('"""')


def main():
    with open("bestiary-mm.json") as f:
        bestiary = load(f)
    monsters = bestiary["monster"]
    for i, monster in enumerate(monsters):
        name = monster["name"]
        print(f"Creating {name}")
        size_dict = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}
        m_type = monster["type"]
        if not isinstance(m_type, str):
            m_type = "{} ({})".format(m_type["type"], ", ".join(m_type["tags"]))
        alignment_dict = {"L": "lawful", "N": "neutral", "C": "chaotic", "G": "good", "E": "evil", "U": "unaligned", "A": "any alignment"}
        if monster["alignment"] == ["L", "NX", "C", "NY", "E"]:
            alignment = "any non-good alignment"
        elif monster["alignment"] == ["NX", "C", "G", "NY", "E"]:
            alignment = "any non-lawful alignment"
        elif monster["alignment"] == ["L", "NX", "C", "E"]:
            alignment = "any evil alignment"
        else:
            alignment = " ".join([alignment_dict[a] for a in monster["alignment"]])
        ac_list = []
        for ac in monster["ac"]:
            if isinstance(ac, int):
                ac_list.append(str(ac))
            elif "from" in ac:
                ac_list.append("{} ({})".format(ac["ac"], ", ".join(ac["from"])))
            elif "condition" in ac:
                ac_list.append("{} {}".format(ac["ac"], ac["condition"]))
            else:
                raise ValueError(ac)
        speed_list = []
        if "walk" not in monster["speed"]:
            speed_list.append("0 ft.")
        for speed, val in monster["speed"].items():
            if speed == "canHover":
                continue
            elif speed == "walk":
                speed_list.append(f"{val} ft.")
            else:
                if isinstance(val, int):
                    speed_list.append(f"{speed} {val} ft.")
                else:
                    speed_list.append(f"{speed} {val['number']} ft. {val['condition']}")
        output = [
            f'width = "500px"',
            f'name = "{name}"',
            f'size = "{size_dict[monster["size"]]}"',
            f'type = "{m_type}"',
            f'alignment = "{alignment}"',
            f'armor_class = "{", ".join(ac_list)}"',
            f'hit_points = "{monster["hp"]["average"]} ({monster["hp"]["formula"]})"',
            f'speed = "{", ".join(speed_list)}"',
            f'strength = {monster["str"]}',
            f'dexterity = {monster["dex"]}',
            f'constitution = {monster["con"]}',
            f'intelligence = {monster["int"]}',
            f'wisdom = {monster["wis"]}',
            f'charisma = {monster["cha"]}',
        ]
        if "save" in monster:
            output.append(f'saves = "{dict_to_stats(monster["save"])}"')
        if "skill" in monster:
            output.append(f'skills = "{dict_to_stats(monster["skill"])}"')
        if "vulnerable" in monster:
            output.append(f'damage_vulnerabilities = "{handle_resistances(monster["vulnerable"], "vulnerable")}"')
        if "resist" in monster:
            output.append(f'damage_resistances = "{handle_resistances(monster["resist"], "resist")}"')
        if "immune" in monster:
            output.append(f'damage_immunities = "{handle_resistances(monster["immune"], "immune")}"')
        if "conditionImmune" in monster:
            output.append(f'condition_immunities = "!{handle_resistances(monster["conditionImmune"], "conditionImmune")}"')
        senses = monster.get("senses", []) + [f"passive Perception {monster['passive']}"]
        output.append(f'senses = "{", ".join(senses)}"')
        if "languages" in monster:
            output.append(f'languages = "{", ".join(monster["languages"])}"')
        if "cr" in monster:
            if isinstance(monster["cr"], str):
                cr = handle_cr(monster["cr"])
            else:
                cr = f'{handle_cr(monster["cr"]["cr"])} or {handle_cr(monster["cr"]["cr"])} when encountered in lair'
            output.append(f'challenge = "{cr}"')
        if "spellcasting" in monster:
            output.append(f'spellcasting = """!')
            for spellcasting_type in monster["spellcasting"]:
                handle_entries(output, spellcasting_type["name"], spellcasting_type["headerEntries"])
                output.append("")
                if "will" in spellcasting_type:
                    output.append(f"At will: {', '.join(spellcasting_type['will'])}")
                if "spells" in spellcasting_type:
                    for spell_level, spell_list in spellcasting_type["spells"].items():
                        if spell_level == "0":
                            spell_level = "Cantrips (at will)"
                        else:
                            slots = spell_list["slots"]
                            spell_level = f"{ordinal(spell_level).lower()} ({slots} slot{'s' if slots > 1 else ''})"
                        output.append(f"{spell_level}: {', '.join(spell_list['spells'])}  ")
            output.append(f'"""')
        add_actions_and_stuff(output, monster, "trait", "special_abilities")
        add_actions_and_stuff(output, monster, "action", "actions")
        add_actions_and_stuff(output, monster, "legendary", "legendary_actions")
        add_actions_and_stuff(output, monster, "reaction", "reactions")
        output.append(f'source = "Monster Manual, p. {monster["page"]}"')

        filepath = f"../data/dnd/monster/{title_to_page_name(name)}.toml"
        with open(filepath, 'w') as f:
            f.writelines(line + '\n' for line in output)


if __name__ == "__main__":
    main()
