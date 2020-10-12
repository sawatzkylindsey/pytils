
import json
ORIGINAL_MAKE_ITERENCODE = json.encoder._make_iterencode
import re

from pytils.override import make_iterencode


def patch_json_encode():
    json.encoder._make_iterencode = make_iterencode._make_iterencode


def unpatch_json_encode():
    json.encoder._make_iterencode = ORIGINAL_MAKE_ITERENCODE


def extended_loads(json_string):
    normalized = _normalize_json(json_string)
    return json.loads(normalized)


# Basic support for comments & commas extension on top of json.
# Won't be perfect, but it works for our use cases.
# Notes:
#   https://hjson.github.io/
#       Surprisingly didn't support my simple test example.
#   https://pypi.org/project/jsoncomment/
#       Is unsupported?  Could not find source or documentation.
#   https://gist.github.com/liftoff/ee7b81659673eca23cd9fc0d8b8e68b7
#       Solution here is based off this gist, but much simpler.
REGEX_COMMENT_MULTILINE = re.compile(r"/\*.*?\*/", re.DOTALL | re.MULTILINE)
REGEX_COMMENT = re.compile(r"//.*?([\"{}\[\],])", re.DOTALL | re.MULTILINE)
REGEX_OBJECT_COMMA = re.compile(r"(,)\s*}")
REGEX_LIST_COMMA = re.compile(r"(,)\s*\]")


def _normalize_json(json_string):
    out = json_string

    # Remove multi-line comments "/* .. */".
    out = re.sub(REGEX_COMMENT_MULTILINE, "", out)

    # Remove trailing comments "// ..".
    out = re.sub(REGEX_COMMENT, "\\1", out)

    # Remove trailing object commas '},'.
    out = re.sub(REGEX_OBJECT_COMMA, "}", out)

    # Remove trailing list commas '],'.
    return re.sub(REGEX_LIST_COMMA, "]", out)

