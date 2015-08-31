from unittest import TestCase

from pytils.table import Table
from pytils.invigilator import create_suite


class Tests(TestCase):
    def test_table(self):
        table = Table([], [])
        self.assertEqual(table.header(), [])
        self.assertEqual(table.rows(), [])
        self.assertEqual(table.width(), 0)
        self.assertEqual(table.height(), 0)

        table = Table(["col1", "col2", "col3"], [["1", "2", 3], [4, "5", "6"]])
        self.assertEqual(table.header(), ["col1", "col2", "col3"])
        self.assertEqual(table.rows(), [
            ["1", "2", 3],
            [4, "5", "6"]
        ])
        self.assertEqual(table.width(), 3)
        self.assertEqual(table.height(), 2)

    def test_table_refine(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        expected = Table.load_csv("col1,col2,col3\n1,2,3")

        refined = table.refine("col1", lambda v: v == "1")
        self.assertEqual(refined, expected)

        refined = table.refine("col1", "1")
        self.assertEqual(refined, expected)

    def test_table_column(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        self.assertEqual(table.column("col1"), ["1", "4"])
        self.assertEqual(table.column("col2"), ["2", "5"])
        self.assertEqual(table.column("col3"), ["3", "6"])

    def test_table_convert(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")

        converted = table.convert("col1", lambda v: int(v))
        self.assertEqual(converted.rows(), [
            [1, "2", "3"],
            [4, "5", "6"]
        ])

        converted = table.convert(conversions={"col1": lambda v: int(v)})
        self.assertEqual(converted.rows(), [
            [1, "2", "3"],
            [4, "5", "6"]
        ])

    def test_table_equality(self):
        table_a = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        table_b = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        table_c = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,7")
        table_d = Table.load_csv("col1,col2,col3,\n1,2,3,\n4,5,6,")

        self.assertEqual(table_a, table_b)
        self.assertNotEqual(table_a, table_c)
        self.assertNotEqual(table_a, table_d)


def tests():
    return create_suite(Tests)
