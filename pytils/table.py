from collections import Counter
from csv import reader as csv_reader


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

    def refine(self, name=None, func_match=None, refinements=None):
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
        if conversions is not None:
            if name is not None or func is not None:
                raise ValueError("May only define (name, func) or " \
                    "conversions, but not both.")

            if not isinstance(conversions, dict):
                raise TypeError("Conversions must be a dict.")
        elif name is None or func is None:
            raise ValueError("Must define either (name, func) or " \
                "conversions.")

        conversion = [lambda v: v for i in range(0, self.width())]

        if conversions is None:
            col = self._find(name)
            conversion[col] = func
        else:
            for name, func in conversions.items():
                col = self._find(name)
                conversion[col] = func

        rows = []

        for data in self.rows():
            row = []

            for i in range(0, self.width()):
                row += [conversion[i](data[i])]

            rows += [row]

        return Table(self.header(), rows)

    def narrow(self, names, unique=False):
        data = self.column_rows(names, unique=unique)
        return Table(names, data)

    def join(self, name, other_table, other_name):
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
        if self.header() != other_table.header():
            raise ValueError("For tables to merge they must have the same header.")

        rows = self.rows()
        rows += other_table.rows()
        return Table(self.header(), rows)

    def sort(self, name, reverse=False):
        col = self._find(name)
        rows = sorted(self.rows(), key=lambda row: row[col], reverse=reverse)
        return Table(self.header(), rows)

    def column(self, name, limit=None):
        if limit is not None and limit < 0:
            raise ValueError("Limit must be 0 or positive.")

        col = self._find(name)
        return self._columns[col][:limit]

    def column_rows(self, names, limit=None, unique=False):
        columns = [self.column(name, limit) for name in names]
        as_rows = []

        if len(columns) > 0:
            i = 0

            while i < len(columns[0]):
                as_row = []

                for column in columns:
                    as_row += [column[i]]

                if as_row not in as_rows or not unique:
                    as_rows += [as_row]

                i += 1

        return as_rows

    def width(self):
        return len(self.header())

    def height(self):
        return len(self.rows())

    def header(self):
        return [h for h in self._header]

    def rows(self):
        return [[d for d in row] for row in self._rows]

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

        for row in self.column_rows(headings):
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
    def load_csv(csv, conversions=None):
        if isinstance(csv, str):
            reader = csv_reader(csv.split("\n"))
        else:
            reader = csv_reader(csv)

        header = None
        rows = []

        for data in reader:
            if header is None:
                header = data
            else:
                rows += [data]

        base = Table(header, rows)

        if conversions is not None:
            return base.convert(conversions=conversions)
        else:
            return base

