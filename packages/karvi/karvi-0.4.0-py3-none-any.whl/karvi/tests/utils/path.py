from unittest import TestCase
from karvi.utils.path import Path


class TestPath(TestCase):
    def test_equals(self):
        p = Path(__file__)
        q = Path(__file__)
        self.assertEqual(p, q)
