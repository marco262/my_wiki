import os

import re

import requests

with open("../data/dragon_heist/gm_notes/gm-notes.md") as f:
    text = f.read()

output_text = text[:]

for m in re.finditer(r"\[(.*?)\]\(\^(.*?)\)", text):
    url = m.group(2)
    if not url.startswith("http"):
        # Check that existing links actually point somewhere
        if not os.path.isfile("../media/img/visual_aids/" + url):
            print("Missing file: " + url)
    if url.startswith("http"):
        if not m.group(1).isdigit():
            name = m.group(1)
            name = name.lower()
            name = re.sub(r"[^a-z ]", "", name)
            name = name.replace("  ", " ").replace(" ", "_")
            print(name)
            r = requests.get(url)
            print(r.status_code)
            if r.status_code == 200:
                content_type = r.headers['content-type']
                extension = content_type.replace("image/", "")
                if extension == "jpeg":
                    extension = "jpg"
                filepath = "/media/img/visual_aids/{}.{}".format(name, extension)
                print(filepath)
                with open(".." + filepath, "wb") as f:
                    f.write(r.content)
                output_text = output_text.replace(m.group(0), "[{}](^{})".format(m.group(1), filepath))
                # break

with open("../data/dragon_heist/gm_notes/gm-notes.md", "w") as f:
    f.write(output_text)
