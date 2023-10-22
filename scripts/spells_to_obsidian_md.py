"""
Usage: python spells_to_obsidian_md.py <output directory>

Creates MD files using the template below and other rules, from the spell TOML files in this repository.
Creates folders within the output directory named "Cantrip", "Level 1", "Level 2", etc and puts MD files in
those by level. Must be run from within the `scripts` directory of this repository.
Will replace any existing files with the same name in that directory.
"""
import os
import re
from argparse import ArgumentParser
from glob import glob
from typing import Iterator

import toml


TEMPLATE = """---
tags:
{tags}
---

*{school_and_level}*
**Casting Time:** {casting_time}
**Range:** {range}
**Components:** {components}{material_component}
**Duration:** {duration}{concentration}{ritual}

{description}{at_higher_levels}

*Source: {source}*
"""


def main():
    args = parse_args()
    for spell in iter_spell_dicts():
        folder_name = "Cantrip" if spell["level"] == "cantrip" else f"Level {spell['level']}"
        os.makedirs(os.path.join(args.output_directory, folder_name), exist_ok=True)
        md = make_spell_md(spell)
        filename = f"{spell['title']}.md"
        filename = filename.replace("/", "-")
        output_filepath = os.path.join(args.output_directory, folder_name, filename)
        with open(output_filepath, "w") as f:
            f.write(md)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("output_directory", help="The directory where the Obsidian MD files should be written to.")
    return parser.parse_args()


def iter_spell_dicts() -> Iterator[dict]:
    for filepath in glob("../data/dnd/spell/*.toml"):
        with open(filepath) as f:
            yield toml.load(f)


def make_spell_md(spell: dict) -> str:
    tags = [f"  - spell/{c}" for c in spell["classes"]]
    if spell.get("concentration_spell"):
        tags.append("  - concentration")
    if spell.get("ritual_spell"):
        tags.append("  - ritual")
    if spell["level"] == "cantrip":
        school_and_level = f"{spell['school']} cantrip"
    else:
        school_and_level = f"{ordinal(int(spell['level']))} level {spell['school']}"
    material_component = f" ({spell['material']})" if "material" in spell else ""
    regex = r"(?<!increases by )(\d*d\d+(\s*[+-]\s*\d+)*)"
    description = re.sub(regex, r"`dice: \1`", spell["description"])
    return TEMPLATE.format(
        tags="\n".join(tags),
        school_and_level=school_and_level,
        casting_time=spell["casting_time"],
        range=spell["range"],
        components=", ".join(spell["components"]),
        material_component=material_component,
        duration=spell["duration"],
        concentration="\n**Concentration**: Yes" if spell.get("concentration_spell") else "",
        ritual="\n**Ritual**: Yes" if spell.get("ritual_spell") else "",
        description=description,
        at_higher_levels=f"\n\n**At higher levels:** {spell['at_higher_levels']}" if spell.get("at_higher_levels") else "",
        source=spell["source"],
    )


def ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


if __name__ == '__main__':
    main()
