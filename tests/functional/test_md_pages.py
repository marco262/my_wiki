import os
import sys
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
        file_count = 0
        for dirname, subdirs, files in os.walk("data"):
            for filename in files:
                file_count += 1
                if not filename.endswith(".md"):
                    continue
                split_dirs = dirname.replace("\\", "/").split("/", 2)
                data_dir = split_dirs[1]
                subdir = split_dirs[2] if len(split_dirs) > 2 else None
                name = os.path.splitext(filename)[0]
                try:
                    md_page(name, namespace=data_dir, directory=subdir)
                except Exception:
                    print(f"Error when building markdown for file {os.path.join(dirname, filename)}", file=sys.stderr)
                    raise
        print(f"Validated {file_count} files")
