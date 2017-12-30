#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
from csv import reader as csv_reader
import random


INDEXING = "indexing"


class Table(object):
    def __init__(self, header=[], rows=[]):
        super(Table, self).__init__()
        self._header = header
        self._rows = rows
        self._columns = [[] for i in range(0, self.width())]

        for row in self._rows:
            if self.width() != len(row):
                raise ValueError("All rows must have exactly %d items.  " \
                    "Found one with %d items." % (self.width(), len(row)))

            for i in range(0, self.width()):
                self._columns[i] += [row[i]]

        header_set = set(self._header)

        if len(header_set) < len(self._header):
            duplicates = self.header()

            for h in header_set:
                duplicates.remove(h)

            raise ValueError("Each header must be uniquely named.  " \
                "Found duplicates: [%s]." % ",".join(duplicates))

    def refine(self, name=None, func_match=None, refinements=None):
        """Produce a table, including only the rows matching some criteria.
        """
        if refinements is not None:
            if name is not None or func_match is not None:
                raise ValueError("May only define (name, func_match) or " \
                    "refinements, but not both.")

            if not isinstance(refinements, dict):
                raise TypeError("refinements must be a dict.")
        elif name is None or func_match is None:
            raise ValueError("Must define either (name, func_match) or " \
                "refinements.")

        refinement = [lambda v: True for i in range(0, self.width())]

        if refinements is None:
            col = self._find(name)
            refinement[col] = func_match
        else:
            for name, func_match in refinements.items():
                col = self._find(name)
                refinement[col] = func_match

        rows = []

        for data in self.rows():
            all_match = True

            for i in range(0, self.width()):
                if callable(refinement[i]):
                    all_match &= refinement[i](data[i])
                else:
                    all_match &= refinement[i] == data[i]

            if all_match:
                rows += [data]

        return Table(self.header(), rows)

    def convert(self, name=None, func=None, conversions=None):
        """Produce a table with values based on some transformations.
        """
        if conversions is not None:
            if name is not None or func is not None:
                raise ValueError("May only define (name, func) or " \
                    "conversions, but not both.")

            if not isinstance(conversions, dict):
                raise TypeError("Conversions must be a dict.")
        elif name is None or func is None:
            raise ValueError("Must define either (name, func) or " \
                "conversions.")

        transformations = [lambda v: v for i in range(0, self.width())]

        if conversions is None:
            col = self._find(name)
            transformations[col] = func
        else:
            for name, func in conversions.items():
                col = self._find(name)
                transformations[col] = func

        rows = []

        for data in self.rows():
            row = []

            for i in range(0, len(transformations)):
                row += [transformations[i](data[i])]

            rows += [row]

        return Table(self.header(), rows)

    def extend(self, names=None, func=None, target=None, extensions=None):
        """Produce a table with new columns based on some transformations.
        """
        if extensions is not None:
            if names is not None or func is not None and target is not None:
                raise ValueError("May only define (names, func, target) or " \
                    "extensions, but not both.")

            if not isinstance(extensions, list):
                raise TypeError("Extensions must be a list.")
        elif names is None or func is None or target is None:
            raise ValueError("Must define either (names, func, target) or " \
                "extensions.")

        transformations = []

        if extensions is None:
            transformations += [{
                "cols": [self._find(name) for name in names],
                "func": func,
                "target": target
            }]
        else:
            for ext in extensions:
                transformations += [{
                    "cols": [self._find(name) for name in ext["names"]],
                    "func": ext["func"],
                    "target": ext["target"]
                }]

        extended_headers = [trans["target"] for trans in transformations]
        rows = []

        for data in self.rows():
            row = [d for d in data]

            for trans in transformations:
                sources = [data[col] for col in trans["cols"]]
                row += [trans["func"](*sources)]

            rows += [row]

        return Table(self.header() + extended_headers, rows)

    def narrow(self, names, unique=False):
        """Produce a table, including only a the columns specified.
        """
        data = self.rows(names, unique=unique)
        return Table(names, data)

    def drop(self, names, unique=False):
        """Produce a table including all columns except those specified.
        """
        columns = self.header()

        for name in names:
            columns.remove(name)

        return self.narrow(columns, unique)

    def join(self, name, other_table, other_name):
        """Produce a table which is the 'inner join' of this and another table.
        """
        values = Counter(self.column(name)).keys()
        other_values = Counter(other_table.column(other_name)).keys()

        rows = []

        for value in values:
            if value in other_values:
                value_table = self.refine(name, value)
                other_value_table = other_table.refine(other_name, value)

                for data in value_table.rows():
                    for other_data in other_value_table.rows():
                        rows += [data + other_data]

        return Table(self.header() + other_table.header(), rows)

    def merge(self, other_table):
        """Produce a table which is the combination of this and another table.
        """
        if self.header() != other_table.header():
            raise ValueError("For tables to merge they must have the same header.")

        rows = self.rows()
        rows += other_table.rows()
        return Table(self.header(), rows)

    def top(self, n):
        rows = []

        if n <= 0:
            return Table(self.header(), rows)

        i = 0

        for data in self.rows():
            rows += [data]
            i += 1

            if i >= n:
                break

        return Table(self.header(), rows)

    def bottom(self, n):
        rows = []
        i = 0
        c = self.height() - n

        for data in self.rows():
            if i >= c:
                rows += [data]

            i += 1

        return Table(self.header(), rows)

    def sort(self, name, reverse=False):
        col = self._find(name)
        rows = sorted(self.rows(), key=lambda row: row[col], reverse=reverse)
        return Table(self.header(), rows)

    def shuffle(self):
        rows = self.rows()
        random.shuffle(rows)
        return Table(self.header(), rows)

    def column(self, name, limit=None):
        if limit is not None and limit < 0:
            raise ValueError("Limit must be 0 or positive.")

        col = self._find(name)
        return self._columns[col][:limit]

    def width(self):
        return len(self.header())

    def height(self):
        return len(self.rows())

    def header(self):
        return [h for h in self._header]

    def rows(self, names=None, limit=None, unique=False):
        headers = self.header()

        if names is not None:
            headers = names

        columns = [self.column(name, limit) for name in headers]
        as_rows = []

        if len(columns) > 0:
            row_index = 0

            while row_index < len(columns[0]):
                as_row = []

                for column in columns:
                    as_row += [column[row_index]]

                if as_row not in as_rows or not unique:
                    as_rows += [as_row]

                row_index += 1

        return as_rows

    def draw(self, names=None):
        if names is None:
            headings = self.header()
        else:
            # Might as well quickly iterate these to make sure they are valid
            for name in names:
                self._find(name)

            headings = names

        lengths = [len(name) for name in headings]
        format_str = "|".join(["{:%d.%ds}" % (l, l) for l in lengths])
        lines = [format_str.format(*headings)]

        for row in self.rows(headings):
            lines += [format_str.format(*[str(r) for r in row])]

        return "\n".join(lines)

    def _find(self, name):
        i = self._header.index(name)

        if i < 0 or i >= self.width():
            raise ValueError("No column found by name '%s'." % name)

        return i

    def __eq__(self, other):
        return self.header() == other.header() and self.rows() == other.rows()

    def __str__(self):
        return "Table: (width=%d, height=%d)" % (self.width(), self.height())

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    @staticmethod
    def load_csv(csv, conversions=None, rename_strategy=None):
        if isinstance(csv, str):
            reader = csv_reader(csv.split("\n"))
        else:
            reader = csv_reader(csv)

        header = None
        rows = []

        for data in reader:
            if header is None:
                header = data

                if rename_strategy is not None:
                    header = Table.rename(header, rename_strategy)
            else:
                rows += [data]

        base = Table(header, rows)

        if conversions is not None:
            return base.convert(conversions=conversions)
        else:
            return base

    @staticmethod
    def rename(header, rename_strategy):
        renamed_header = [name for name in header]

        if rename_strategy == INDEXING:
            counts = Counter(header)
            indexes = {}
            renamed_header = []

            for name in header:
                if counts[name] > 1:
                    if name not in indexes:
                        indexes[name] = 0

                    renamed_header += ["%s_%s" % (name, indexes[name])]
                    indexes[name] += 1
                else:
                    renamed_header += [name]

        return renamed_header

