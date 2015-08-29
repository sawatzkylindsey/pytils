from unittest import TestCase

from pytils.test import create_suite


class Tests(TestCase):
    def test_things(self):
        self.assertEqual(0, 1)


def tests():
    return create_suite(Tests)
