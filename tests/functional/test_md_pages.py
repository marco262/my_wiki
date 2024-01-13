import os
from unittest import TestCase
from unittest.mock import patch

from src.common.markdown_parser import MarkdownParser
from src.common.utils import md_page
from tests.unit import find_root_directory


class TestMdPages(TestCase):

    @classmethod
    def setUpClass(cls):
        find_root_directory()
        cls.md = MarkdownParser()

    @patch("src.common.utils.redirect")
    def test_build_md_pages(self, *_mocks):
        """
        Automatically builds all markdown pages to verify there are no errors thrown during conversion
        """
        for dirname, subdirs, files in os.walk("data"):
            for filename in files:
                if not filename.endswith(".md"):
                    continue
                split_dirs = dirname.replace("\\", "/").split("/", 2)
                data_dir = split_dirs[1]
                subdir = split_dirs[2] if len(split_dirs) > 2 else None
                filename = os.path.splitext(filename)[0]
                md_page(filename, namespace=data_dir, directory=subdir)
