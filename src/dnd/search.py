import re
from os import walk
from os.path import join


class Search:

    def __init__(self):
        pass

    def run(self, search_term):
        results = []
        for dirpath, dirnames, filenames in walk("data/dnd"):
            for filename in filenames:
                if filename.endswith(".md") or filename.endswith(".toml"):
                    filepath = join(dirpath, filename)
                    with open(filepath, "rb") as f:
                        m = re.search(search_term, f.read().decode("utf-8"))
                        if m:
                            results.append([dirpath, filename])