#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import os
import pstats
import sys


def main():
    ap = ArgumentParser(prog="stats")
    ap.add_argument("--count", "-c", type=int, default=20, help="Limit by count of lines, defaults to 20.")
    ap.add_argument("--sort", "-s", default="cumtime")
    ap.add_argument("profile_file")
    ap.add_argument("restriction", nargs="?")
    args = ap.parse_args(sys.argv[1:])

    if not os.path.exists(args.profile_file):
        return 1

    p = pstats.Stats(args.profile_file)
    p.strip_dirs().sort_stats(args.sort).print_stats(args.count, args.restriction)
    return 0


if __name__ == "__main__":
    sys.exit(main())

