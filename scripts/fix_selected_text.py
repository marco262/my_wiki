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
elif sys.argv[1] == "add_spell":
    text = text.lower()
    text = re.sub(r"^", "_[[[spell:", text)
    text = re.sub(r"$", "]]]_", text)
elif sys.argv[1] == "add_special_formatting":
    text = text.replace("\r", "")
    text = re.sub(r" = !!!", ' = """!', text)
    text = re.sub(r"!!!", '"""', text)
    text = re.sub(r'([a-z_]+) = ([^\"].*[a-zA-Z].*)', r'\1 = "\2"', text)
else:
    raise Exception("Unknown function: {}".format(sys.argv[1]))

print(text)
clipboard.copy(text)
