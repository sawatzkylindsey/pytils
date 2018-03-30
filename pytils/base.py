#!/usr/bin/python
# -*- coding: utf-8 -*-

import operator


class Comparable(object):
    def __init__(self, *args, **kwargs):
        super(Comparable, self).__init__(*args, **kwargs)

    def _comparator(self, fn, other):
        # Typical implementations will look like this:
        #   return fn((self.attribute1, .., self.attributeN), (other.attribute1, .., other.attributeN))
        class_str = str(self.__class__)
        class_name = class_str.split("'")[1]
        raise NotImplementedError("%s._comparator" % class_name)

    def __lt__(self, other):
        return self._comparator(operator.lt, other)

    def __le__(self, other):
        return self._comparator(operator.le, other)

    def __gt__(self, other):
        return self._comparator(operator.gt, other)

    def __ge__(self, other):
        return self._comparator(operator.ge, other)

