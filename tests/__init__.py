
from pytils.invigilator import create_suite
from tests import adjutant, base, check, stream, table


def all():
    return create_suite(unit())


def unit():
    return [
        adjutant.tests(),
        base.tests(),
        check.tests(),
        stream.tests(),
        table.tests(),
    ]
