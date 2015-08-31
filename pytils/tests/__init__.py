from pytils.invigilator import create_suite
from pytils.tests import table


def all():
    return create_suite(unit())


def unit():
    return [
        table.tests()
    ]
