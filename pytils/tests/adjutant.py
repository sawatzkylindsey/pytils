from unittest import TestCase

from pytils.adjutant import dict_as_str
from pytils.invigilator import create_suite


class Tests(TestCase):
    def test_dict_as_str(self):
        # ints
        d = {"a": 3, "b": 1, "c": 2}
        self.assertEqual(dict_as_str(d, True, False), "{a: 3, b: 1, c: 2}")
        self.assertEqual(dict_as_str(d, False, False), "{b: 1, c: 2, a: 3}")
        self.assertEqual(dict_as_str(d, True, True), "{c: 2, b: 1, a: 3}")
        self.assertEqual(dict_as_str(d, False, True), "{a: 3, c: 2, b: 1}")
        # strs
        self.assertEqual(dict_as_str({"a": "jack", "b": "bob"}), "{a: jack, b: bob}")
        self.assertEqual(dict_as_str({"a": "jack", "b": "bob"}, False), "{b: bob, a: jack}")


def tests():
    return create_suite(Tests)

