#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import math


def check_not_none(value):
    if value is None:
        raise ValueError("value is unexpectedly None")

    return value


def check_none(value):
    if value is not None:
        raise ValueError("value '%s' is unexpectedly not None" % value)

    return value


def check_not_empty(value):
    if len(value) == 0:
        raise ValueError("value '%s' is unexpectedly empty" % value)

    if isinstance(value, str) and len(value.lstrip()) == 0:
        raise ValueError("value '%s' is unexpectedly only whitespace" % value)

    return value


def check_not_contains(value, substr):
    if substr in value:
        raise ValueError("value '%s' unexpectedly contains '%s'" % (value, susbstr))

    return value


def check_not_instance(value, instance):
    if isinstance(value, instance):
        raise ValueError("value '%s' is unexpectedly an instance '%s'" % (value, instance))

    return value


def check_instance(value, instance):
    if not isinstance(value, instance):
        raise ValueError("value '%s' is unexpectedly not an instance '%s'" % (value, instance))

    return value


def check_list(value):
    if not isinstance(value, list):
        raise ValueError("value '%s' is unexpectedly not a list" % value)

    return value


def check_set(value):
    if not isinstance(value, set):
        raise ValueError("value '%s' is unexpectedly not a set" % value)

    return value


def check_list_or_set(value):
    if not isinstance(value, list) and not isinstance(value, set):
        raise ValueError("value '%s' is unexpectedly not a list or a set" % value)

    return value


def check_dict(value):
    if not isinstance(value, dict):
        raise ValueError("value '%s' is unexpectedly not a dict" % value)

    return value


def check_iterable(value):
    try:
        discard = iter(value)
    except TypeError as e:
        raise ValueError("value '%s' is unexpectedly not iterable" % value)

    return value


def check_iterable_of_instances(value, instance):
    for v in check_iterable(value):
        if not isinstance(v, instance):
            raise ValueError("item '%s' is unexpectedly not an instance '%s'" % (v, instance))

    return value


def check_not_equal(value, other):
    if value == other:
        raise ValueError("value '%s' is unexpectedly equal to '%s'" % (value, other))

    return value


def check_equal(value, other):
    if value != other:
        raise ValueError("value '%s' is unexpectedly not equal to '%s'" % (value, other))

    return value


def check_lte(value, target):
    if value > target:
        raise ValueError("value '%s' is unexpectedly not less than or equal to '%s'" % (value, target))

    return value


def check_gte(value, target):
    if value < target:
        raise ValueError("value '%s' is unexpectedly not greater than or equal to '%s'" % (value, target))

    return value


def check_lt(value, target):
    if value >= target:
        raise ValueError("value '%s' is unexpectedly not less than '%s'" % (value, target))

    return value


def check_gt(value, target):
    if value <= target:
        raise ValueError("value '%s' is unexpectedly not greater than '%s'" % (value, target))

    return value


def check_length(value, expected):
    if len(value) != expected:
        raise ValueError("value '%s' ('%d') is unexpectedly not of length '%d'" % (value, len(value), expected))

    return value


def check_one_of(value, options):
    if value not in options:
        raise ValueError("value '%s' is unexpectedly not one of '%s'" % (value, options))

    return value


def check_pdist(value):
    # Assume some iterable
    probabilities = value

    if isinstance(value, dict):
        probabilities = value.values()

    if not math.isclose(1.0, sum(probabilities), abs_tol=0.005):
        raise ValueError("value '%s' unexpectedly does not represent a probability distribution" % (probabilities))

    return value

