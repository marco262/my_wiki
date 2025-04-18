import re
import sys
from typing import List

import clipboard

from src.common.utils import better_title

if len(sys.argv) < 2:
    raise Exception("Pass in a function to run, you goddamn moron")

text = clipboard.paste()
arg = sys.argv[1]

if arg == "create_wiki_spell_table":
    text = text.lower().replace("\r", "")
    text = re.sub(r"^", "|| ", text, flags=re.MULTILINE)
    text = re.sub(r" \s+", " || _[[[spell:", text)
    text = re.sub(r", ", "]]]_, _[[[spell:", text)
    text = re.sub(r"$", "]]]_ ||", text, flags=re.MULTILINE)
elif arg == "create_wiki_table":
    text = text.replace("\r", "")
    text = re.sub(r"^", "|| ", text, flags=re.MULTILINE)
    text = re.sub(r"( \s+|\t+)", " || ", text)
    text = re.sub(r"$", " ||@", text, flags=re.MULTILINE)
    first_line = text.split("\n")[0]
    first_line_repl = first_line.replace("|| ", "||~ ")
    text = text.replace(first_line, first_line_repl)
elif arg == "fix_line_breaks":
    text = re.sub(r"’", "'", text)
    text = re.sub(r"“", '"', text)
    text = re.sub(r"”", '"', text)
    text = re.sub(r"[ϐϔ]", "f", text)
    text = re.sub(r"●", "*", text)
    text = re.sub(r"•", "*", text)
    text = re.sub(r"¦", "fi", text)
    text = re.sub(r"§", "fl", text)
    text = re.sub(r"¨", "ffi", text)
    text = re.sub(r"©", "ffi", text)
    text = re.sub(r" ?— ?", " -- ", text)
    # 3 RD L EVEL: B ONUS P ROFICIENCIES => ### 3rd Level: Bonus Proficiencies
    for m in re.finditer(r"(\d+)(st|nd|rd|th) L ?EVEL:(.*)", text, re.IGNORECASE | re.MULTILINE):
        feature_name = m.group(3).strip(" ").lower()
        feature_name_words: List[str] = feature_name.split(" ")
        feature_name = " ".join([word.title() if word not in ["of"] else word for word in feature_name_words])
        text = text.replace(m.group(0), f"@@### {m.group(1)}{m.group(2).lower()} Level: {feature_name}@@")
    # LEVEL 4: ABILITY SCORE IMPROVEMENT => ### Level 4: Ability Score Improvement
    for m in re.finditer(r"L ?EVEL (\d+):(.*)", text, re.IGNORECASE | re.MULTILINE):
        feature_name = m.group(2).strip(" ").lower()
        feature_name_words: List[str] = feature_name.split(" ")
        feature_name = " ".join([word.title() if word not in ["of"] else word for word in feature_name_words])
        # Fix issue where the first letter of words has an erroneous space
        for m2 in re.finditer(r"\b([A-Z]) ([A-Z])", feature_name):
            feature_name = feature_name.replace(m2.group(0), m2.group(1) + m2.group(2).lower())
        text = text.replace(m.group(0), f"@@### Level {m.group(1)}: {feature_name}@@")
    # CREATURE TYPE => # Creature Type
    # for m in re.finditer(r"^[A-Z\s\[\]]+$", text, re.MULTILINE):
    #     text = text.replace(m.group(0), f"@@# {better_title(m.group(0)).strip()}@@")
    text = re.sub(r"\r?\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"@ ", "@", text)
    text = re.sub(r" *@", "\n", text)
elif arg == "add_spells":
    text = ", ".join([f"_[[[spell:{t}]]]_" for t in text.split(", ")])
elif arg == "glossary":
    text = f"[[glossary:{text}]]"
elif arg == "add_special_formatting":
    for m in re.finditer(r'^(.*?),', text, re.MULTILINE):
        title = m.group(1).capitalize()
        for n in re.finditer(r" ([a-z])", title):
            title = title.replace(n.group(0), f" {n.group(1).upper()}")
        for n in re.finditer(r"\(([a-z])", title):
            title = title.replace(n.group(0), f"({n.group(1).upper()}")
        text = text.replace(m.group(0), f'{title},')
elif arg == "invocations":
    text = re.sub(r"\r?\n", "|", text)
    for m in re.finditer(r"([ A-Z']+)\|Prerequisite: (.*?)\|", text, re.MULTILINE):
        name = better_title(m.group(1).lower())
        header_text = f"@@## {name}@@|_Prerequisite: {m.group(2)}_@@|"
        text = text.replace(m.group(0), header_text)
    text = text.replace("|", "\n")
elif arg == "create_ability_list":
    for m in re.finditer(r"^(.*?)\. ", text, re.MULTILINE):
        text = text.replace(m.group(0), f"* **{m.group(1)}.** ")
elif arg == "create_onednd_spell_list":
    reg = r"(\d) (.*?) (\S+) (Yes|No)"
    lines = []
    for m in re.finditer(reg, text, re.MULTILINE):
        school = m.group(3).replace("Transmut.", "Transmutation")
        spell = m.group(2).replace("’", "'").replace("†", "").replace("‡", "")
        lines.append(f"|  {m.group(1)}  | _[[[spell:{spell}]]]_ | {school} | {m.group(4)} |")
    text = "\n".join(lines)
elif arg == "title":
    text = "### " + " ".join([s.title() for s in text.split(" ")])
else:
    raise Exception("Unknown function: {}".format(arg))

print(text)
clipboard.copy(text)
