from unittest import TestCase

from pytils import base
from pytils.invigilator import create_suite


class TestObject(base.Comparable):
    def __init__(self, stuff, things):
        super(TestObject, self).__init__()
        self.stuff = stuff
        self.things = things

    def _comparator(self, fn, other):
        return fn((self.stuff, self.things), (other.stuff, other.things))


class Tests(TestCase):
    def test_comparable(self):
        a_1 = TestObject("a", 1)
        a_2 = TestObject("a", 2)
        b_1 = TestObject("b", 1)

        self.assertLessEqual(a_1, a_1)
        self.assertGreaterEqual(a_1, a_1)
        self.assertLess(a_1, a_2)
        self.assertLess(a_1, b_1)

        self.assertGreater(a_2, a_1)
        self.assertLessEqual(a_2, a_2)
        self.assertGreaterEqual(a_2, a_2)
        self.assertLess(a_2, b_1)

        self.assertGreater(b_1, a_1)
        self.assertGreater(b_1, a_2)
        self.assertLessEqual(b_1, b_1)
        self.assertGreaterEqual(b_1, b_1)


def tests():
    return create_suite(Tests)

