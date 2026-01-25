import re

from json import load, dumps

from src.common.utils import title_to_page_name


ITEM_CACHE = {}


def clean_markdown(text: str) -> str:
    text = re.sub(r"{@damage (.*?)}", r"\1", text)
    text = re.sub(r"{@(variantrule|action|condition|status|sense|hazard) (.*?)( \[.*?])?\|XPHB(\|.*?)?}", r"[[glossary:\2]]", text)
    text = re.sub(r"{@item Artisan's Tools\|XPHB}", r"[[[general:equipment#artisans-tools|Artisan's Tools]]]", text)
    text = re.sub(r"{@skill (.*?)( \[.*?])?\|(XPHB|XDMG)(\|.*?)?}", r"[[tooltip:\1]]", text)
    text = re.sub(r"{@item (.*?)( \[.*?])?\|(XPHB|XDMG)(\|.*?)?}", r"[[tooltip:\1]]", text)
    text = re.sub(r"{@creature (.*?)( \[.*?])?\|.*?}", r"[[[monster:\1]]]", text)
    text = re.sub(r"{@race (.*?)( \[.*?])?\|.*?}", r"[[[advancement:Races#\1]]]", text)
    text = re.sub(r"{@spell (.*?)\|.*?}", r"[[[spell:\1]]]", text)
    text = re.sub(r"{@filter (.*?)\|.*?}", r"\1", text)
    text = re.sub(r"{@dice (.*?)}", r"\1", text)
    text = re.sub(r"{@dc (.*?)}", r"DC \1", text)
    text = re.sub(r"{@(scaledamage|scaledice) .*?\|.*?\|(.*?)}", r"\2", text)
    text = re.sub(r"{@chance (.*?)\|.*?}", r"\1 percent chance", text)
    text = re.sub(r"{@book (.*?)\|.*?}", r"\1", text)
    text = re.sub(r"{@b (.*?)}", r"**\1**", text)
    text = re.sub(r"{@i (.*?)}", r"_\1_", text)
    text = re.sub(r"{@hit (.*?)}", r"+\1", text)
    text = text.replace("—", " -- ")
    # Fix glossary misnomers
    text = text.replace("[[glossary:Opportunity Attack]]", "[[glossary:Opportunity Attacks|Opportunity Attack]]")
    return text


def join_with_or(items: list) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} or {items[1]}"
    return f"{', '.join(items[:-1])}, or {items[-1]}"


def parse_entries(entries: list[str | dict], entry_templates: dict = None, item: dict = None) -> str:
    text_list = []
    for e in entries:
        if isinstance(e, str):
            m = re.match(r"\{#itemEntry (.*?)\|.*?}", e)
            if m:
                matching_name = m.group(1)
                desc = entry_templates[matching_name]
                if "resist" in item:
                    desc = desc.replace("{{getFullImmRes item.resist}}", item["resist"][0])
                if "detail1" in item:
                    desc = desc.replace("{{item.detail1}}", item["detail1"])
                if "detail2" in item:
                    desc = desc.replace("{{item.detail2}}", item["detail2"])
                assert "{{" not in desc, desc
                text_list.append(desc)
            else:
                text_list.append(e)
        elif e["type"] == "list":
            inner_list = []
            for item in e["items"]:
                if isinstance(item, str):
                    inner_list.append(" - " + item)
                elif item["type"] == "item":
                    inner_list.append(f" - **{item['name']}.** {parse_entries(item['entries'])}")
                else:
                    raise ValueError(e)
            text_list.append("\n".join(inner_list))
        elif e["type"] == "entries":
            text_list.append(f"**_{e['name']}._** " + parse_entries(e["entries"]))
        elif e["type"] == "table":
            if "caption" in e:
                text_list.append(f'**{e["caption"]}**')
            text_list.append(make_table(e))
        elif e["type"] == "inset":
            text_list.append("[[sidebar]]")
            text_list.append(parse_entries(e["entries"]))
            text_list.append("[[/sidebar]]")
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


def parse_spells():
    SPELLS_PATH = "../../5etools-src/data/spells/spells-efa.json"
    CLASS_LIST_PATH = "../../5etools-src/data/spells/sources.json"

    with open(SPELLS_PATH) as f:
        spells = load(f)

    with open(CLASS_LIST_PATH) as f:
        spell_class_lists = load(f)["EFA"]

    for spell in spells["spell"]:
        name = spell["name"]
        print(name)

        source_list = spell_class_lists[name]["class"]
        spell_lists = []
        for d in source_list:
            if d["source"] == "TCE":
                continue
            spell_lists.append(d["name"])
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


def parse_monsters():
    MONSTERS_PATHS = [
        "../../5etools-src/data/bestiary/bestiary-xphb.json",
        "../../5etools-src/data/bestiary/bestiary-xdmg.json",
        "../../5etools-src/data/bestiary/bestiary-xmm.json",
    ]
    monsters = {}
    for path in MONSTERS_PATHS:
        with open(path) as f:
            monsters.update(load(f))


def parse_magic_items():
    MAGIC_ITEMS_PATH = "../../5etools-src/data/items-base.json"

    with open(MAGIC_ITEMS_PATH) as f:
        item_entries = load(f)

    # Parse item entries
    entry_templates = {}
    for item in item_entries["itemEntry"]:
        if item["source"] in ("XDMG", "EFA"):
            entry_templates[item["name"]] = parse_entries(item["entriesTemplate"])

    MAGIC_ITEMS_PATH = "../../5etools-src/data/items.json"

    with open(MAGIC_ITEMS_PATH, "rb") as f:
        magic_items = load(f)

    for magic_item in magic_items["item"]:
        if magic_item["source"] == "XDMG":
            source = "Dungeon Master's Guide"
        elif magic_item["source"] == "EFA":
            source = "Eberron: Forge of the Artificer"
        else:
            continue
        name = magic_item["name"]
        if name.startswith("+"):
            num, name = name.split(" ", 1)
            name = name + ", " + num
        subtype = ""
        if magic_item.get("wondrous"):
            type_ = "Wondrous Item"
        elif magic_item.get("staff"):
            type_ = "Staff"
        elif "type" in magic_item:
            type_, _ = magic_item["type"].split("|")
            match type_:
                case "M":
                    type_ = "Weapon"
                case "LA":
                    type_ = "Armor"
                case "MA":
                    type_ = "Armor"
                case "HA":
                    type_ = "Armor"
                case "S":
                    type_ = "Armor"
                case "P":
                    type_ = "Potion"
                case "SC":
                    type_ = "Scroll"
                case "RG":
                    type_ = "Ring"
                case "RD":
                    type_ = "Rod"
                case "WD":
                    type_ = "Wand"
                case "$A":
                    # Skip art object
                    continue
                case "$G":
                    # Skip gemstones
                    continue
                case "G":
                    # Skip poison???
                    continue
                case "EXP":
                    # Skip explosives
                    continue
                case "TB":
                    # Skip trade bar?
                    continue
                case "TG":
                    # Skip trade good
                    continue
                case _:
                    raise ValueError(type_)
        else:
            raise ValueError(f"No type found for {name}")
        if "baseItem" in magic_item:
            item_name, _ = magic_item["baseItem"].split("|")
            subtype = " ".join([w.title() for w in item_name.split(" ")])
        rarity = magic_item["rarity"].title()
        if "lootTables" in magic_item:
            tables = [s.split("-")[0].strip() for s in magic_item["lootTables"]]
            assert rarity != "Artifact"
        elif rarity == "Artifact":
            # Artifacts shouldn't be on the loot table
            pass
        elif source != "Dungeon Master's Guide":
            # Non-DMG items don't show up in loot tables
            pass
        else:
            # Exceptions to make my life easier
            if "Bag of Tricks" in name:
                tables = ["Arcana"]
            elif "Carpet of Flying" in name:
                tables = ["Arcana", "Implements"]
            elif "Dragon Scale Mail" in name:
                tables = ["Armaments"]
            elif "Elemental Gem" in name:
                tables = ["Arcana"]
            elif name.startswith("Potion of ") and name.endswith(" Resistance"):
                tables = ["Arcana", "Relics"]
            elif name.startswith("Ring of ") and name.endswith(" Resistance"):
                tables = ["Relics"]
            elif "Scroll of Protection" in name:
                tables = ["Arcana", "Relics"]
            elif "Scroll of Titan Summoning" in name:
                tables = ["Arcana", "Relics"]
            else:
                print(f"Missing loot tables: {name} ({rarity})")
                tables = []
        attunement = str(bool(magic_item.get("reqAttune"))).lower()
        classes = []
        for d in magic_item.get("reqAttuneTags", []):
            if "class" in d:
                classes.append(d["class"].title())
            elif d == {"spellcasting": True}:
                classes.append("spellcaster")
        notes = ""
        page_num = magic_item['page']

        output = f"""name = "{name}"
type = "{type_}"
subtype = "{subtype}"
rarity = "{rarity}"
tables = {dumps(tables)}
attunement = {attunement}
classes = {dumps(classes)}
notes = "{notes}"
source = "{source}, p. {page_num}"
"""

        desc = parse_entries(magic_item["entries"], entry_templates, magic_item)
        if "\n" not in desc and '"' not in desc:
            output += f'description = "{desc}"\n'
        else:
            output += f'description = """\n{desc}\n"""\n'

        filepath = f"../data/dnd/equipment/magic-items/{title_to_page_name(name)}.toml"
        with open(filepath, "wb") as f:
            f.write(output.encode())


def parse_magic_item_variants():
    MAGIC_ITEMS_PATH = "../../5etools-src/data/items-base.json"

    with open(MAGIC_ITEMS_PATH) as f:
        item_entries = load(f)

    # Parse item entries
    entry_templates = {}
    for item in item_entries["itemEntry"]:
        if item["source"] in ("XDMG", "EFA"):
            entry_templates[item["name"]] = parse_entries(item["entriesTemplate"])

    MAGIC_ITEMS_PATH = "../../5etools-src/data/magicvariants.json"

    with open(MAGIC_ITEMS_PATH) as f:
        magic_items = load(f)

    for magic_item in magic_items["magicvariant"]:
        name = magic_item["name"]
        if name.startswith("+"):
            num, name = name.split(" ", 1)
            name = name + ", " + num
        if " (*)" in name:
            name = name.replace(" (*)", "")

        variant_item = magic_item["inherits"]
        if variant_item["source"] == "XDMG":
            source = "Dungeon Master's Guide"
        elif variant_item["source"] == "EFA":
            source = "Eberron: Forge of the Artificer"
        else:
            continue

        type_, _ = magic_item["type"].split("|")
        assert type_ == "GV"
        subtype = ""
        if "requires" in magic_item:
            if magic_item["requires"] == [{"weapon": True}]:
                type_ = "Weapon"
                subtype = "Any Simple or Martial"
            elif magic_item["requires"] == [{"sword": True}]:
                type_ = "Weapon"
                subtype = "Greatsword, Longsword, Rapier, Scimitar, or Shortsword"
            else:
                requires = []
                add_any = False
                property = ""
                for req in magic_item["requires"]:
                    if "type" in req:
                        req_type = req["type"].split("|")[0]
                        if req_type == "M":
                            type_ = "Weapon"
                            add_any = True
                            requires.append("Melee Weapon")
                        elif req_type == "A":
                            requires.append("Ammunition")
                            type_ = "Weapon"
                        elif req_type == "AF":
                            pass
                        elif req_type == "LA":
                            type_ = "Armor"
                            add_any = True
                            requires.append("Light")
                        elif req_type == "MA":
                            type_ = "Armor"
                            add_any = True
                            requires.append("Medium")
                        elif req_type == "HA":
                            type_ = "Armor"
                            add_any = True
                            requires.append("Heavy")
                        elif req_type == "S":
                            type_ = "Armor"
                            requires.append("Shield")
                        else:
                            raise ValueError(req)
                    elif "name" in req:
                        requires.append(req["name"])
                        # Hack for missing data
                        if req["name"] in ("Battleaxe", "Shortbow", "Greatsword", "Warhammer", "Dagger"):
                            type_ = "Weapon"
                        elif req["name"] in ("Half Plate Armor", "Chain Mail"):
                            type_ = "Armor"
                    elif "weaponCategory" in req:
                        type_ = "Weapon"
                        add_any = True
                        requires.append(req["weaponCategory"].title())
                        if "property" in req:
                            if req["property"] == "A|XPHB":
                                property = "Ammunition"
                            elif req["property"] == "T|XPHB":
                                property = "Thrown"
                assert requires
                if add_any:
                    subtype += "Any "
                subtype += join_with_or(requires)
                if property:
                    subtype += f" with the {property} Property"
        if "excludes" in magic_item:
            subtype += f", Except {magic_item['excludes']['name']}"

        assert type_ != "GV", magic_item

        rarity = variant_item["rarity"].title()
        if "lootTables" in variant_item:
            tables = [s.split("-")[0].strip() for s in variant_item["lootTables"]]
            assert rarity != "Artifact"
        elif rarity == "Artifact":
            # Artifacts shouldn't be on the loot table
            pass
        elif source != "Dungeon Master's Guide":
            # Non-DMG items don't show up in loot tables
            pass
        else:
            # Exceptions to make my life easier
            if re.match(r"Armor of \w+ Resistance", name):
                tables = ["Armaments"]
            elif r"Armor of Vulnerability" in name:
                tables = ["Armaments"]
            else:
                print(f"Missing loot tables: {name} ({rarity})")
                tables = []
        attunement = str(bool(variant_item.get("reqAttune"))).lower()
        classes = []
        for d in variant_item.get("reqAttuneTags", []):
            if "class" in d:
                classes.append(d["class"].title())
            elif d == {"spellcasting": True}:
                classes.append("spellcaster")
        notes = ""
        page_num = variant_item['page']

        output = f"""name = "{name}"
type = "{type_}"
subtype = "{subtype}"
rarity = "{rarity}"
tables = {dumps(tables)}
attunement = {attunement}
classes = {dumps(classes)}
notes = "{notes}"
source = "{source}, p. {page_num}"
"""

        desc = parse_entries(variant_item["entries"], entry_templates, variant_item)
        if "{=bonusAc}" in desc:
            desc = desc.replace("{=bonusAc}", variant_item["bonusAc"])
        if "{=bonusWeapon}" in desc:
            desc = desc.replace("{=bonusWeapon}", variant_item["bonusWeapon"])
        if "\n" not in desc:
            output += f'description = "{desc}"\n'
        else:
            output += f'description = """\n{desc}\n"""\n'

        filepath = f"../data/dnd/equipment/magic-items/{title_to_page_name(name)}.toml"
        with open(filepath, "w") as f:
            f.write(output)


if __name__ == '__main__':
    # parse_spells()
    # parse_monsters()
    parse_magic_items()
    parse_magic_item_variants()
