from os import walk
from os.path import join, splitext, basename

import re
import toml

from src.common.utils import strip_html


class Search:

    def __init__(self, context_length=50):
        self.context_length = context_length
        self.cache = {}

    def add_context_to_search_term(self, search_term):
        # Add 4 to context length to account for ellipses that will be added for too-long contexts.
        context_length = self.context_length + 4
        context_string = r"(.{," + str(context_length) + "})"
        return re.compile("{context_string}({search_term}){context_string}".format(
            search_term=search_term, context_string=context_string
        ), re.IGNORECASE)

    def build_results_context_string(self, re_match):
        """
        :param re_match: 3-tuple matching the search: (N characters before, search term, N characters after)
        :return:
        """
        before = strip_html(re_match[0])
        if len(before) > self.context_length:
            before = "..." + before[-1 * self.context_length:]
        after = strip_html(re_match[2])
        if len(after) > self.context_length:
            after = after[:self.context_length] + "..."
        return f"{before}<strong>{re_match[1]}</strong>{after}"

    def run(self, search_term):
        if search_term in self.cache:
            return self.cache[search_term]
        results = self.do_search(search_term)
        # Sort results by number of matches, and path
        # Number of matches should be in descending order (pages with more matches at the top)
        # but path should be in ascending order (a before z)
        results.sort(key=lambda x: (-1*len(x[3]), x[2]))
        self.cache[search_term] = results
        return results

    def do_search(self, search_term):
        results = []
        search_term_with_context = self.add_context_to_search_term(search_term)
        for dirpath, dirnames, filenames in walk("data/dnd"):
            for filename in filenames:
                if filename.endswith(".md") or filename.endswith(".toml"):
                    result = self.search_file(dirpath, filename, search_term_with_context)
                    if result:
                        results.append(result)
        return results

    def search_file(self, dirpath, filename, search_term_with_context):
        # Read file contents
        filepath = join(dirpath, filename)
        with open(filepath, "rb") as f:
            file_contents = f.read().decode("utf-8")
        # Search for search term in file
        m = re.findall(search_term_with_context, file_contents)
        if not m:
            return None
        # Attempt to pull title out of TOML file, otherwise generate title from filename
        title = None
        if filename.endswith(".toml"):
            d = toml.loads(file_contents)
            if "title" in d:
                title = d["title"]
        if not title:
            title = splitext(filename)[0].replace("-", " ").title()
        # Build search results
        filepath = join(dirpath, filename).replace("\\", "/")
        html_link = f"/dnd/{basename(dirpath)}/{title}"
        contexts = [self.build_results_context_string(match) for match in m]
        return [title, filepath, html_link, contexts]
