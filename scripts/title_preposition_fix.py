from glob import glob
from os.path import basename
from re import search, sub

for path in glob("../data/spell/*"):
    with open(path) as f:
        contents = f.read()
    old_title = search(r'title = "(.*)"', contents)
    title = old_title.group(1)

    prepositions = ["of", "and", "to", "a", "an", "in", "the"]
    for p in prepositions:
        pattern = r"\b" + p.title() + r"\b"
        title = sub(pattern, p, title)
    title = title.split(" ")
    # Always capitalize first and last words of a title
    title[0] = title[0].capitalize()
    title[-1] = title[-1].capitalize()
    title = " ".join(title)
    if old_title.group(1) != title:
        print(f"{old_title.group(1)} => {title}")
        contents = contents.replace(old_title.group(0), f'title = "{title}"')
        with open(path, 'w') as f:
            f.write(contents)
