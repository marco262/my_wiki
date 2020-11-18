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
    text = re.sub(r" \s+", " || ", text)
    text = re.sub(r"$", " ||", text, flags=re.MULTILINE)
elif sys.argv[1] == "fix_line_breaks":
    text = re.sub(r"’", "'", text)
    text = re.sub(r"“", '"', text)
    text = re.sub(r"”", '"', text)
    text = re.sub(r"[ϐ|ϔ]", "f", text)
    text = re.sub(r"●", "*", text)
    text = re.sub(r"\r?\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"@ ", "@", text)
    text = re.sub(r"@", "\n", text)
elif sys.argv[1] == "add_spell":
    text = text.lower()
    text = re.sub(r"^", "_[[[spell:", text)
    text = re.sub(r"$", "]]]_", text)
elif sys.argv[1] == "make_invocations":
    lines = []
    for i, line in enumerate(re.split("\r?\n", text)):
        if line.startswith("Prerequisite"):
            lines.append("_" + line + "_")
        elif line and line == line.upper():
            new_line = []
            for word in line.split(" "):
                if word in ("OF", "THE"):
                    new_line.append(word.lower())
                else:
                    new_line.append(word.title())
            lines.append("### " + " ".join(new_line))
        else:
            lines.append(line)
    text = "\n".join(lines)
else:
    raise Exception("Unknown function: {}".format(sys.argv[1]))

print(text)
clipboard.copy(text)
