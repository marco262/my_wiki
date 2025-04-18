import re
from os import walk
from os.path import join, splitext, basename
from typing import NamedTuple, List, Optional

import toml

from src.common.utils import strip_html, title_to_page_name, page_name_to_title


class SearchResult(NamedTuple):
    title: str
    filepath: str
    html_link: str
    contexts: Optional[List[str]]


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
        results.sort(key=lambda x: (-1 * len(x[3]), x[2]))
        # Bucket results whose name matches the search term exactly, whose name contains the search term,
        # and all others.
        exact_matches = []
        partial_matches = []
        other_matches = []
        search_term = search_term.lower()
        for r in results:
            name = r[0].lower()
            if search_term == name:
                exact_matches.append(r)
            elif search_term in name:
                partial_matches.append(r)
            else:
                other_matches.append(r)
        results = exact_matches + partial_matches + other_matches
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
            title = page_name_to_title(splitext(filename)[0])
        return self.build_search_result(dirpath, filename, title, m)

    def build_search_result(self, dirpath, filename, title, regex_matches=None):
        filepath = join(dirpath, filename).replace("\\", "/")
        base_dir = basename(dirpath)
        if base_dir == "magic-items":
            base_dir = "equipment/magic-item"
        html_link = f"/dnd/{base_dir}/{title}"
        # Return only the first ten contexts
        if regex_matches is not None:
            contexts = [self.build_results_context_string(match) for match in regex_matches][:10]
        else:
            contexts = None
        return SearchResult(title, filepath, html_link, contexts)

    def page_search(self, search_term):
        """
        Returns results for only "exact" page name matches. "Exact" is in quotes because markdown pages
        lose proper punctuation when converting to page names, so the search term "Scout (Fighter)" will
        return the same page as "Scout Fighter".
        """
        search_as_page_name = title_to_page_name(search_term)
        results = []
        for dirpath, dirnames, filenames in walk("data/dnd"):
            for filename in filenames:
                if filename.endswith(".md") and search_as_page_name in filename:
                    title = page_name_to_title(splitext(filename)[0])
                elif filename.endswith(".toml") and search_as_page_name in filename:
                    filepath = join(dirpath, filename)
                    with open(filepath, "rb") as f:
                        file_contents = f.read().decode("utf-8")
                    d = toml.loads(file_contents)
                    title = d.get("title") or d.get("name")
                else:
                    continue
                search_result = self.build_search_result(dirpath, filename, title)
                # If this is an exact match, just redirect to that page
                if search_as_page_name == splitext(filename)[0]:
                    return search_result.html_link
                results.append(search_result)
        return results
