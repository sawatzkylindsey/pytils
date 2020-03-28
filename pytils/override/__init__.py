
import json
ORIGINAL_MAKE_ITERENCODE = json.encoder._make_iterencode

from pytils.override import make_iterencode


def patch_json_encode():
    json.encoder._make_iterencode = make_iterencode._make_iterencode


def unpatch_json_encode():
    json.encoder._make_iterencode = ORIGINAL_MAKE_ITERENCODE

