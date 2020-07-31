from unittest import TestCase

from pytils.stream import randomize
from pytils.invigilator import create_suite


class Tests(TestCase):
    def test_randomize_smaller(self):
        items = [i for i in range(10)]
        modified_a = [i for i in randomize(items, 100)]
        modified_b = [i for i in randomize(items, 100)]

        self.assertNotEqual(modified_a, items)
        self.assertNotEqual(modified_b, items)
        self.assertNotEqual(modified_a, modified_b)
        self.assertEqual(sorted(modified_a), items)
        self.assertEqual(sorted(modified_b), items)

    def test_randomize_bigger(self):
        items = [i for i in range(10)]
        modified_a = [i for i in randomize(items, 100)]
        modified_b = [i for i in randomize(items, 100)]

        self.assertNotEqual(modified_a, items)
        self.assertNotEqual(modified_b, items)
        self.assertNotEqual(modified_a, modified_b)
        self.assertEqual(sorted(modified_a), items)
        self.assertEqual(sorted(modified_b), items)

    def test_randomize_one(self):
        items = [i for i in range(10)]
        modified_a = [i for i in randomize(items, 1)]
        modified_b = [i for i in randomize(items, 1)]

        self.assertEqual(modified_a, items)
        self.assertEqual(modified_b, items)


def tests():
    return create_suite(Tests)

