import unittest

from src.common.utils import better_title


class TestUtils(unittest.TestCase):

    def test_better_title(self):
        data = "a player's guide and an equal treatment of the sexes"
        expected = "A Player's Guide and an Equal Treatment of the Sexes"
        self.assertEqual(expected, better_title(data))
