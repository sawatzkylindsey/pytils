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
        self.assertEqual(table.draw(), "")

        table = Table(["col1", "col2", "col3"], [["1", "2", 3], [4, "5", "6"]])
        self.assertEqual(table.header(), ["col1", "col2", "col3"])
        # Make sure it is immutable
        h = table.header()
        h += ["header"]
        self.assertEqual(table.header(), ["col1", "col2", "col3"])
        self.assertEqual(table.rows(), [
            ["1", "2", 3],
            [4, "5", "6"]
        ])
        # Make sure it is immutable
        r = table.rows()
        r += [["abc", "x", "y"]]
        self.assertEqual(table.rows(), [
            ["1", "2", 3],
            [4, "5", "6"]
        ])
        # Make sure the inner row is immutable
        r = table.rows()
        r[0] += ["abc"]
        self.assertEqual(table.rows(), [
            ["1", "2", 3],
            [4, "5", "6"]
        ])
        self.assertEqual(table.width(), 3)
        self.assertEqual(table.height(), 2)
        self.assertEqual(table.draw(),
            "col1|col2|col3\n1   |2   |3   \n4   |5   |6   ")

        table = Table(["col1", "col2", "col3"],
            [["1", "2asdf", 3], [4, "5", "6"]])
        self.assertEqual(table.draw(),
            "col1|col2|col3\n1   |2asd|3   \n4   |5   |6   ")
        self.assertEqual(table.draw(["col1", "col2", "col3"]),
            "col1|col2|col3\n1   |2asd|3   \n4   |5   |6   ")
        self.assertEqual(table.draw(["col1", "col3"]),
            "col1|col3\n1   |3   \n4   |6   ")
        self.assertEqual(table.draw(["col3", "col1"]),
            "col3|col1\n3   |1   \n6   |4   ")
        self.assertEqual(table.draw(["col3"]),
            "col3\n3   \n6   ")
        self.assertEqual(table.draw([]),
            "")

    def test_table_refine(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        expected = Table.load_csv("col1,col2,col3\n1,2,3")

        refined = table.refine("col1", lambda v: v == "1")
        self.assertEqual(refined, expected)

        refined = table.refine("col1", "1")
        self.assertEqual(refined, expected)

        refined = table.refine(refinements={"col1": lambda v: v == "1"})
        self.assertEqual(refined, expected)

        refined = table.refine(refinements={"col1": "1"})
        self.assertEqual(refined, expected)

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

    def test_table_sort(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,1,6")

        sortd = table.sort("col1")
        self.assertEqual(sortd.rows(), [
            ["1", "2", "3"],
            ["4", "1", "6"]
        ])
        sortd = table.sort("col1", reverse=True)
        self.assertEqual(sortd.rows(), [
            ["4", "1", "6"],
            ["1", "2", "3"]
        ])

        sortd = table.sort("col2")
        self.assertEqual(sortd.rows(), [
            ["4", "1", "6"],
            ["1", "2", "3"]
        ])
        sortd = table.sort("col2", reverse=True)
        self.assertEqual(sortd.rows(), [
            ["1", "2", "3"],
            ["4", "1", "6"]
        ])

        table = Table(["col"], [["2"], ["1"], [None]])
        sortd = table.sort("col")
        self.assertEqual(sortd.rows(), [
            [None],
            ["1"],
            ["2"]
        ])
        sortd = table.sort("col", reverse=True)
        self.assertEqual(sortd.rows(), [
            ["2"],
            ["1"],
            [None]
        ])

    def test_table_column(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        self.assertEqual(table.column("col1"), ["1", "4"])
        self.assertEqual(table.column("col2"), ["2", "5"])
        self.assertEqual(table.column("col3"), ["3", "6"])

        self.assertEqual(table.column("col1", 0), [])
        self.assertEqual(table.column("col1", 1), ["1"])
        self.assertEqual(table.column("col1", 2), ["1", "4"])
        self.assertEqual(table.column("col1", 3), ["1", "4"])

    def test_table_column_rows(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6")
        self.assertEqual(table.column_rows(["col1", "col2"]), [["1", "2"], ["4", "5"]])
        self.assertEqual(table.column_rows(["col3", "col2"]), [["3", "2"], ["6", "5"]])
        self.assertEqual(table.column_rows(["col3"]), [["3"], ["6"]])
        self.assertEqual(table.column_rows([]), [])

        self.assertEqual(table.column_rows(["col1", "col2"], 1), [["1", "2"]])

    def test_table_narrow(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6\n4,5,7")
        self.assertEqual(table.narrow(["col1", "col2"]).rows(), [["1", "2"], ["4", "5"], ["4", "5"]])
        self.assertEqual(table.narrow(["col1", "col2"], unique=True).rows(), [["1", "2"], ["4", "5"]])
        self.assertEqual(table.narrow(["col3", "col2"]).rows(), [["3", "2"], ["6", "5"], ["7", "5"]])
        self.assertEqual(table.narrow(["col3"]).rows(), [["3"], ["6"], ["7"]])
        self.assertEqual(table.narrow([]).rows(), [])

        self.assertEqual(table.narrow(["col1", "col2"]).rows(), [["1", "2"], ["4", "5"], ["4", "5"]])

    def test_table_join(self):
        table_a = Table.load_csv("id,name\n1,alice\n2,bob\n3,eve")
        table_b = Table.load_csv("fid,spirit\n1,virtuous\n1,delightful\n3,evil\n0,moot")
        joined = table_a.join("id", table_b, "fid")

        self.assertEqual(joined.header(), ["id", "name", "fid", "spirit"])
        self.assertEqual(joined.sort("spirit").rows(), [
            ["1", "alice", "1", "delightful"],
            ["3", "eve", "3", "evil"],
            ["1", "alice", "1", "virtuous"]
        ])

    def test_table_merge(self):
        table_1 = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6",
            {"col1": lambda v: int(v)})
        table_2 = Table.load_csv("col1,col2,col3\n7,8,9\n10,11,12")
        table = table_1.merge(table_2)

        self.assertEqual(table.rows(), [
            [1, "2", "3"],
            [4, "5", "6"],
            ["7", "8", "9"],
            ["10", "11", "12"]
        ])

    def test_table_load_csv(self):
        table = Table.load_csv("col1,col2,col3\n1,2,3\n4,5,6",
            {"col1": lambda v: int(v)})

        self.assertEqual(table.header(), ["col1", "col2", "col3"])
        self.assertEqual(table.rows(), [
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
