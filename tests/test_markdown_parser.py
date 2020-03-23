import os
import unittest
from unittest import mock

from src.common.markdown_parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MarkdownParser(init_md=False)
        cls.md.namespace = "dnd"

    def test_base_dir(self):
        from src.common.markdown_parser import BASE_DIR
        self.assertEqual("my_wiki", os.path.basename(BASE_DIR))

    def test_convert_wiki_links(self):
        pre_markdown = """
        [[[class:cleric#toc|Table of Contents]]]
        [[[class:cleric#domains]]]
        [[[class:cleric]]]
        [[[Mutants]]]
        """
        expected = """
        <a class="wiki-link" href="/dnd/class/cleric#toc">Table of Contents</a>
        <a class="wiki-link" href="/dnd/class/cleric#domains">domains</a>
        <a class="wiki-link" href="/dnd/class/cleric">cleric</a>
        <a class="wiki-link" href="/dnd/Mutants">Mutants</a>
        """
        actual = self.md.convert_wiki_links(pre_markdown)
        self.assertEqual(expected, actual)

    @mock.patch("os.path.isfile")
    def test_check_wiki_links(self, *mocks):
        def mock_func(path):
            path = path.replace("\\", "/")  # Normalize OS paths
            return path.endswith(r"my_wiki/data/dnd/class/cleric.md") or path.endswith(r"my_wiki/data/dnd/mutants.md")

        isfile_mock = mocks[0]
        isfile_mock.side_effect = mock_func
        html = """
        <a class="wiki-link" href="/dnd/class/fake_cleric#toc">Table of Contents</a>
        <a class="wiki-link" href="/dnd/class/cleric#domains">domains</a>
        <a class="wiki-link" href="/dnd/class/fake_cleric">cleric</a>
        <a class="wiki-link" href="/dnd/Mutants">Mutants</a>
        """
        expected = """
        <a class="wiki-link-broken" href="/dnd/class/fake_cleric#toc">Table of Contents</a>
        <a class="wiki-link" href="/dnd/class/cleric#domains">domains</a>
        <a class="wiki-link-broken" href="/dnd/class/fake_cleric">cleric</a>
        <a class="wiki-link" href="/dnd/Mutants">Mutants</a>
        """
        self.assertEqual(expected, self.md.check_wiki_links(html))

    def test_parse_accordion(self):
        pre_markdown = """
[[accordion Test Title]]
# Header

* Item 1
* *Item 2*
* **Item 3**

Text block

[[/accordion]]
"""
        expected = """<button class="accordion-button">Test Title</button>
<div class="accordion-panel">

<h1 id="header">Header</h1>

<ul>
<li>Item 1</li>
<li><em>Item 2</em></li>
<li><strong>Item 3</strong></li>
</ul>

<p>Text block</p>

</div>
"""
        md = MarkdownParser()
        actual = md.parse_md(pre_markdown)
        self.assertEqual(expected, actual)
