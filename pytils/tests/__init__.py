from pytils.invigilator import create_suite
from pytils.tests import base, check, table


def all():
    return create_suite(unit())


def unit():
    return [
        base.tests(),
        check.tests(),
        table.tests(),
    ]
