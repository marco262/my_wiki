import re
from os import walk
from os.path import join, splitext, basename

import toml

from src.common.utils import title_to_filename


class Search:

    title_results = []
    results = []

    def __init__(self, context_length=50):
        self.context_length = context_length
        self.cache = {}

    def add_context_to_search_term(self, search_term):
        # Add 4 to context length to account for ellipses that will be added for too-long contexts.
        context_length = self.context_length + 4
        context_string = r"(.{," + str(context_length) + "})"
        search_string = "{context_string}({search_term}){context_string}".format(
            search_term=search_term, context_string=context_string
        )
        return re.compile(search_string, re.IGNORECASE)

    def build_results_context_string(self, re_match):
        before = re_match.group(1)
        if len(before) > self.context_length:
            before = "..." + before[-1 * self.context_length:]
        after = re_match.group(3)
        if len(after) > self.context_length:
            after = after[:self.context_length] + "..."
        return f"{before}<strong>{re_match.group(2)}</strong>{after}"

    def run(self, search_term):
        if search_term in self.cache:
            return self.cache[search_term]
        results = self.do_search(search_term)
        self.cache[search_term] = results
        return results

    def add_to_results(self, dirpath, filename, context):
        filepath = join(dirpath, filename)
        title = None
        if filename.endswith(".toml"):
            with open(filepath) as f:
                d = toml.loads(f.read())
                if "title" in d:
                    title = d["title"]
        if not title:
            title = splitext(filename)[0].replace("-", " ").title()
        html_link = f"/dnd/{basename(dirpath)}/{title}"
        filepath = filepath.replace("\\", "/")
        if context:
            self.results.append([title, filepath, html_link, context])
        else:
            self.title_results.append([title, filepath, html_link, context])

    def do_search(self, search_term):
        self.title_results = []
        self.results = []
        search_term_with_context = self.add_context_to_search_term(search_term)
        for dirpath, dirnames, filenames in walk("data/dnd"):
            for filename in filenames:
                if filename.endswith(".md") or filename.endswith(".toml"):
                    if title_to_filename(search_term) in filename.lower():
                        self.add_to_results(dirpath, filename, "")
                    else:
                        with open(join(dirpath, filename), "rb") as f:
                            m = re.search(search_term_with_context, f.read().decode("utf-8"))
                            if m:
                                context = self.build_results_context_string(m)
                                self.add_to_results(dirpath, filename, context)
        return self.title_results + self.results
