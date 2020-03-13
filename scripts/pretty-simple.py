#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import json
import pdb
import sys

from pytils import io
from pytils.override import make_iterencode


def main(argv):
    ap = ArgumentParser(prog="pretty-simple.py")
    ap.add_argument("source", nargs="?", help="Input file or standard in.")
    ap.add_argument("-i", "--indent", default=4, type=int)
    aargs = ap.parse_args(argv)
    pretty_simplify(aargs.source, aargs.indent)
    return 0


def pretty_simplify(source, indent):
    original_make_iterencode = json.encoder._make_iterencode

    try:
        generator = io.stdin_generator() if source is None else io.file_generator(source)
        json.encoder._make_iterencode = make_iterencode._make_iterencode
        print(json.dumps(json.loads("".join(generator)), indent=indent, separators=(", ", ": ")))
    finally:
        json.encoder._make_iterencode = original_make_iterencode


if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)

