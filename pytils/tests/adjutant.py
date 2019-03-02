from unittest import TestCase

from pytils.adjutant import dict_as_str
from pytils.invigilator import create_suite


class Tests(TestCase):
    def test_dict_as_str_sort(self):
        # str-int
        d = {"a": 3, "b": 1, "c": 2}
        self.assertEqual(dict_as_str(d, True, False), "{a: 3, b: 1, c: 2}")
        self.assertEqual(dict_as_str(d, False, False), "{b: 1, c: 2, a: 3}")
        self.assertEqual(dict_as_str(d, True, True), "{c: 2, b: 1, a: 3}")
        self.assertEqual(dict_as_str(d, False, True), "{a: 3, c: 2, b: 1}")

    def test_dict_as_str_combinations(self):
        # str-str
        d = {"a": "jack", "b": "bob"}
        self.assertEqual(dict_as_str(d), "{a: jack, b: bob}")

        # int-float
        d = {1: .51234, 2: -1.2}
        self.assertEqual(dict_as_str(d), "{1: 0.5123, 2: -1.2000}")

        # float-str
        d = {.51234: "jack", -1.2: "bob"}
        self.assertEqual(dict_as_str(d), "{-1.2000: bob, 0.5123: jack}")

        # str-dict
        d = {"a": {1: "jack", 2: "bob"}, "b": {3: "alice", 4: "jacob"}}
        self.assertEqual(dict_as_str(d), "{a: {1: jack, 2: bob}, b: {3: alice, 4: jacob}}")
        self.assertEqual(dict_as_str(d, reverse=True), "{b: {4: jacob, 3: alice}, a: {2: bob, 1: jack}}")

        # str-tuple
        d = {"a": (2, 3), "b": (1, 2)}
        self.assertEqual(dict_as_str(d), "{a: (2, 3), b: (1, 2)}")
        self.assertEqual(dict_as_str(d, False), "{b: (1, 2), a: (2, 3)}")

    def test_dict_as_str_unsortable(self):
        try:
            dict_as_str({"a": {}}, sort_by_key=False)
            raise AssertionError("unexpected success")
        except ValueError as e:
            # Expected
            pass


def tests():
    return create_suite(Tests)

