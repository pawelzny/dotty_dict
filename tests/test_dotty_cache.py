import unittest
from unittest.mock import MagicMock

from dotty_dict import dotty


class TestDottyCache(unittest.TestCase):

    def test_getitem_cache(self):
        dot = dotty()
        dot._data = MagicMock()
        for _ in range(10):
            dot.get('x.y.z')
        self.assertEqual(dot.__getitem__.cache_info().hits, 9)
