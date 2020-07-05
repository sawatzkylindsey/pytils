#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
import math
import os


check_on = "pytils_check_on" in os.environ


def activate():
    global check_on
    check_on = True


def check_not_none(value):
    if check_on:
        if value is None:
            raise ValueError("value is unexpectedly None")

    return value


def check_none(value):
    if check_on:
        if value is not None:
            raise ValueError("value '%s' is unexpectedly not None" % str(value))

    return value


def check_not_empty(value, noneable=False):
    if check_on:
        if len(value) == 0 and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly empty%s" % (str(value), _suffix_noneable(noneable)))

        if isinstance(value, str) and len(value.lstrip()) == 0 and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly only whitespace%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_not_contains(value, substr):
    if check_on:
        if substr in value:
            raise ValueError("value '%s' unexpectedly contains '%s'" % (str(value), str(susbstr)))

    return value


def check_not_instance(value, instance):
    if check_on:
        if isinstance(value, instance):
            raise ValueError("value '%s' is unexpectedly an instance %s" % (str(value), str(instance)))

    return value


def check_instance(value, instance_s, noneable=False):
    if check_on:
        if _is_iterable(instance_s):
            if not any([isinstance(value, i) for i in instance_s]) and _violates_noneable(value, noneable):
                raise ValueError("value '%s' is unexpectedly not an instance %s%s" % (str(value), " or ".join([str(i) for i in instance_s]), _suffix_noneable(noneable)))
        else:
            if not isinstance(value, instance_s) and _violates_noneable(value, noneable):
                raise ValueError("value '%s' is unexpectedly not an instance %s%s" % (str(value), instance_s, _suffix_noneable(noneable)))

    return value


def check_list(value, noneable=False):
    if check_on:
        if not isinstance(value, list) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not a list%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_set(value, noneable=False):
    if check_on:
        if not isinstance(value, set) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not a set%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_list_or_set(value, noneable=False):
    if check_on:
        if not isinstance(value, list) and not isinstance(value, set) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not a list or a set%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_dict(value, noneable=False):
    if check_on:
        if not isinstance(value, dict) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not a dict%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_iterable(value, noneable=False):
    if check_on:
        if not _is_iterable(value) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not iterable%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_iterable_of_instances(value, instance_s, noneable=False):
    if check_on:
        if value is not None:
            for v in check_iterable(value):
                if _is_iterable(instance_s):
                    if not any([isinstance(v, i) for i in instance_s]):
                        raise ValueError("item '%s' inside iterable is unexpectedly not an instance %s" % (str(v), " or ".join([str(i) for i in instance_s])))
                else:
                    if not isinstance(v, instance_s):
                        raise ValueError("item '%s' inside iterable is unexpectedly not an instance %s" % (str(v), instance_s))
        elif _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexepectedly none" % (str(value)))

    return value


def check_not_equal(value, other):
    if check_on:
        if value == other:
            raise ValueError("value '%s' is unexpectedly equal to '%s'" % (str(value), str(other)))

    return value


def check_equal(value, other):
    if check_on:
        if value != other:
            raise ValueError("value '%s' is unexpectedly not equal to '%s'" % (str(value), str(other)))

    return value


def check_condition(condition, failure_description):
    condition_result = condition

    if check_on:
        if callable(condition):
            condition_result = condition()

        if not condition_result:
            raise ValueError(failure_description)

    return condition_result


def check_function(value, noneable=False):
    if check_on:
        if not callable(value) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not a function%s" % (str(value), _suffix_noneable(noneable)))

    return value


def check_lte(value, target):
    if check_on:
        if value > target:
            raise ValueError("value '%s' is unexpectedly not less than or equal to '%s'" % (str(value), str(target)))

    return value


def check_gte(value, target):
    if check_on:
        if value < target:
            raise ValueError("value '%s' is unexpectedly not greater than or equal to '%s'" % (str(value), str(target)))

    return value


def check_range(value, lower, upper, noneable=False):
    if check_on:
        if (value < lower or value > upper) and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not in range [%s, %s]%s" % (str(value), str(lower), str(upper), _suffix_noneable(noneable)))

    return value


def check_lt(value, target):
    if check_on:
        if value >= target:
            raise ValueError("value '%s' is unexpectedly not less than '%s'" % (str(value), str(target)))

    return value


def check_gt(value, target):
    if check_on:
        if value <= target:
            raise ValueError("value '%s' is unexpectedly not greater than '%s'" % (str(value), str(target)))

    return value


def check_probability(value):
    if check_on:
        if value < 0.0 or value > 1.0:
            raise ValueError("value '%s' is unexpectedly not a probability" % str(value))

    return value


def check_length(value, expected, noneable=False):
    if check_on:
        if value is not None:
            if len(value) != expected:
                raise ValueError("value '%s' ('%d') is unexpectedly not of length '%d'%s" % (str(value), len(value), expected, _suffix_noneable(noneable)))
        elif _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexepectedly none" % (str(value)))


    return value


def check_one_of(value, options, noneable=False):
    if check_on:
        if value not in options and _violates_noneable(value, noneable):
            raise ValueError("value '%s' is unexpectedly not one of '%s'%s" % (str(value), str(options), _suffix_noneable(noneable)))

    return value


def check_pdist(value):
    if check_on:
        # Assume some iterable
        probabilities = value

        if isinstance(value, dict):
            probabilities = value.values()

        if not math.isclose(1.0, sum([check_probability(p) for p in probabilities]), abs_tol=0.005):
            raise ValueError("value '%s' unexpectedly does not represent a probability distribution" % (probabilities))

    return value


def check_exclusive(values):
    matched = [k for k, v in values.items() if v is not None]

    if check_on:
        if len(matched) == 0:
            raise ValueError("values '%s' are unexpectedly not exclusive - none of '%s' were provided" %
                (", ".join([k for k in values.keys()]), ", ".join([k for k in values.keys()])))
        elif len(matched) > 1:
            raise ValueError("values '%s' are unexpectedly not exclusive - all of '%s' were provided" %
                (", ".join([k for k in values.keys()]), ", ".join(matched)))

    return matched[0]


def _is_iterable(thing):
    try:
        discard = iter(thing)
        return True
    except TypeError:
        return False


def _violates_noneable(value, noneable):
    return not noneable or value is not None


def _suffix_noneable(noneable):
    return " or None" if noneable else ""

