#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
import pdb
import sys

from pytils import io
import pytils.override


def main(argv):
    ap = ArgumentParser(prog="pretty-simple.py")
    ap.add_argument("source", nargs="?", help="Input file or standard in.")
    ap.add_argument("-i", "--indent", default=4, type=int)
    aargs = ap.parse_args(argv)
    pretty_simplify(aargs.source, aargs.indent)
    return 0


def pretty_simplify(source, indent):
    try:
        generator = io.stdin_generator() if source is None else io.file_generator(source)
        data = pytils.override.extended_loads("".join(generator))
        pytils.override.patch_json_encode()
        print(json.dumps(data, indent=indent, separators=(", ", ": ")))
    finally:
        pytils.override.unpatch_json_encode()


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)

