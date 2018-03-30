from pytils.invigilator import create_suite
from pytils.tests import check, table


def all():
    return create_suite(unit())


def unit():
    return [
        check.tests(),
        table.tests(),
    ]
