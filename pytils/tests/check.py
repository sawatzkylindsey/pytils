from unittest import TestCase

from pytils import check
from pytils.invigilator import create_suite


class Tests(TestCase):
    def test_check(self):
        try:
            check.check_not_none(None)
            raise AssertionError("unexpected success")
        except ValueError as e:
            self.assertEqual(e.message, "value is unexpectedly None")


def tests():
    return create_suite(Tests)
