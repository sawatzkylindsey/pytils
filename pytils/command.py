
from pytils import check


def as_name(name_or_flags):
    # As input, recieve a name or flags as per: https://docs.python.org/3/library/argparse.html#name-or-flags
    name = name_or_flags

    if name.startswith("--"):
        name = name[2:]
    elif name.startswith("-"):
        name = name[1:]

    return name.replace("-", "_")


class Arg:
    def __init__(self, args, kwargs):
        self.args = check.check_list(args)
        self.kwargs = check.check_dict(kwargs)
        self.name = as_name(sorted(self.args, key=self.argument_sort_key, reverse=True)[0])

    def extract(self, namespace):
        return namespace.__dict__[self.name]

    def add_to(self, arg_parser):
        arg_parser.add_argument(*self.args, **self.kwargs)

    def argument_sort_key(self, item):
        # The sort key for an argument, a string of the form: {"asdf", "--asdf", "-a"}, can be formulated as a triple:
        # (has no dash prefix, has double dash prefix, has single dash prefix)
        return (not item.startswith("-"), item.startswith("--"), item.startswith("-"))

