
import gzip
import sys


def stdin_generator():
    for line in sys.stdin:
        yield line


def file_generator(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as fh:
            for line in fh.readlines():
                yield line
    except UnicodeDecodeError as e:
        with gzip.open(input_file, "rt", encoding="utf-8") as fh:
            for line in fh.readlines():
                yield line

