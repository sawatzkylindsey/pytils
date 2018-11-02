from pytils.invigilator import create_suite
from pytils.tests import adjutant, base, check, table


def all():
    return create_suite(unit())


def unit():
    return [
        adjutant.tests(),
        base.tests(),
        check.tests(),
        table.tests(),
    ]
