import csv

class Table(object):
    def __init__(self, header=[], rows=[]):
        super(Table, self).__init__()
        self._header = header
        self._rows = rows
        self._columns = [[] for i in range(0, self.width())]

        for row in self._rows:
            if self.width() != len(row):
                raise ValueError("All rows must have exactly %d items."
                    % self.width())

            for i in range(0, self.width()):
                self._columns[i] += [row[i]]

    def refine(self, name, func_match):
        col = self._find(name)
        rows = []

        for data in self.rows():
            if callable(func_match) and func_match(data[col]):
                rows += [data]
            elif data[col] == func_match:
                rows += [data]

        return Table(self.header(), rows)

    def convert(self, name=None, func=None, conversions=None):
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

    def column(self, name):
        col = self._find(name)
        return self._columns[col]

    def width(self):
        return len(self.header())

    def height(self):
        return len(self.rows())

    def header(self):
        return self._header

    def rows(self):
        return self._rows

    def _find(self, name):
        i = self._header.index(name)

        if i < 0 or i >= self.width():
            raise ValueError("No column found by name '%s'." % name)

        return i

    def __eq__(self, other):
        return self.header() == other.header() and self.rows() == other.rows()

    def __str__(self):
        return "Table: %s - %s" % (self.header(), self.rows())

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        return str(self)

    @staticmethod
    def load_csv(text):
        reader = csv.reader(text.split("\n"))
        header = None
        rows = []

        for data in reader:
            if header is None:
                header = data
            else:
                rows += [data]

        return Table(header, rows)

