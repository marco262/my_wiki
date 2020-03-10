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
        [Table of Contents](/dnd/class/cleric#toc)
        [domains](/dnd/class/cleric#domains)
        [cleric](/dnd/class/cleric)
        [Mutants](/dnd/Mutants)
        """
        actual = self.md.convert_wiki_links(pre_markdown)
        self.assertEqual(expected, actual)
