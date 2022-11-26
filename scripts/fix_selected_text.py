import re
import sys

import clipboard

if len(sys.argv) == 1:
    raise Exception("Pass in a function to run, you goddamn moron")

text = clipboard.paste()

if sys.argv[1] == "create_wiki_spell_table":
    text = text.lower().replace("\r", "")
    text = re.sub(r"^", "|| ", text, flags=re.MULTILINE)
    text = re.sub(r" \s+", " || _[[[spell:", text)
    text = re.sub(r", ", "]]]_, _[[[spell:", text)
    text = re.sub(r"$", "]]]_ ||", text, flags=re.MULTILINE)
elif sys.argv[1] == "create_wiki_table":
    text = text.replace("\r", "")
    text = re.sub(r"^", "|| ", text, flags=re.MULTILINE)
    text = re.sub(r"( \s+|\t+)", " || ", text)
    text = re.sub(r"$", " ||@", text, flags=re.MULTILINE)
    first_line = text.split("\n")[0]
    first_line_repl = first_line.replace("|| ", "||~ ")
    text = text.replace(first_line, first_line_repl)
elif sys.argv[1] == "fix_line_breaks":
    text = re.sub(r"’", "'", text)
    text = re.sub(r"“", '"', text)
    text = re.sub(r"”", '"', text)
    text = re.sub(r"[ϐϔ]", "f", text)
    text = re.sub(r"●", "*", text)
    text = re.sub(r"¦", "fi", text)
    text = re.sub(r"§", "fl", text)
    text = re.sub(r"¨", "ffi", text)
    text = re.sub(r"©", "ffi", text)
    text = re.sub(r" ?— ?", " -- ", text)
    text = re.sub(r"\r?\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"@ ", "@", text)
    text = re.sub(r"@", "\n", text)
    # 3 RD L EVEL: B ONUS P ROFICIENCIES => ### 3rd Level: Bonus Proficiencies
    for m in re.finditer(r"(\d+) (st|nd|rd|th) L EVEL:(.*)", text, re.IGNORECASE | re.MULTILINE):
        feature_name = m.group(3).lower()
        for n in re.finditer(r" (\w) ", feature_name):
            feature_name = feature_name.replace(n.group(0), " " + n.group(1).upper())
        text = text.replace(m.group(0), f"### {m.group(1)}{m.group(2).lower()} Level:{feature_name}")
elif sys.argv[1] == "add_spell":
    text = text.lower()
    text = re.sub(r"^", "_[[[spell:", text)
    text = re.sub(r"$", "]]]_", text)
    text = re.sub(r", ?", "]]]_, _[[[spell:", text)
elif sys.argv[1] == "add_special_formatting":
    for m in re.finditer(r'^(.*?),', text, re.MULTILINE):
        title = m.group(1).capitalize()
        for n in re.finditer(r" ([a-z])", title):
            title = title.replace(n.group(0), f" {n.group(1).upper()}")
        for n in re.finditer(r"\(([a-z])", title):
            title = title.replace(n.group(0), f"({n.group(1).upper()}")
        text = text.replace(m.group(0), f'{title},')
elif sys.argv[1] == "feats":
    text = text.replace("\r\n", "|")
    for m in re.finditer(r"([ A-Z:]+)\|(.*?)-Level Feat\|Prerequisite: (.*?)\|Repeatable: (.*?)\|", text, re.MULTILINE):
        # print(m.groups())
        name = m.group(1)
        name = name.replace(" ", "").title()
        header_text = f"## {name}@@|*{m.group(2)}-Level Feat*@@|**Prerequisite:** {m.group(3)}  @|**Repeatable:** {m.group(4)}@@|"
        text = text.replace(m.group(0), header_text)
    text = text.replace("|", "\n")
elif sys.argv[1] == "create_ability_list":
    for m in re.finditer(r"^(.*?)\. ", text, re.MULTILINE):
        text = text.replace(m.group(0), f"* **{m.group(1)}.** ")
else:
    raise Exception("Unknown function: {}".format(sys.argv[1]))

print(text)
clipboard.copy(text)
