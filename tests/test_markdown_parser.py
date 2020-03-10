import unittest

from src.common.markdown_parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MarkdownParser(init_md=False)
        cls.md.namespace = "dnd"

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
