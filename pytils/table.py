from csv import reader as csv_reader


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

    def sort(self, name, reverse=False):
        col = self._find(name)
        rows = sorted(self.rows(), key=lambda row: row[col], reverse=reverse)
        return Table(self.header(), rows)

    def column(self, name, limit=None):
        if limit is not None and limit < 0:
            raise ValueError("Limit must be 0 or positive.")

        col = self._find(name)
        return self._columns[col][:limit]

    def columns(self, names, limit=None):
        if len(names) == 0:
            raise ValueError("Must specify at least one name.")

        return [self.column(name, limit) for name in names]

    def width(self):
        return len(self.header())

    def height(self):
        return len(self.rows())

    def header(self):
        return self._header

    def rows(self):
        return self._rows

    def draw(self):
        lengths = [len(name) for name in self.header()]
        format_str = "|".join(["{:.%ds}" % l for l in lengths])
        lines = [format_str.format(*self.header())]

        for row in self.rows():
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

