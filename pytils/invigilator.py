import unittest


def create_suite(tests):
    """Create a unittest test suite.

    Assumes the list of tests is homogenous.

    :param tests: The tests to make a suite out of.
    :type tests: Single :py:class:`unittest.TestCase`,
                 :py:class:`unittest.TestSuite`, or list of either.
    :returns: A :py:class:`unittest.TestSuite` suitable for execution.
    """
    if isinstance(tests, list):
        suite = unittest.TestSuite()

        if len(tests) > 0 and isinstance(tests[0], type):
            for test in tests:
                suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test))
        else:
            suite.addTests(tests)

        return suite
    elif isinstance(tests, unittest.TestSuite):
        return unittest.TestSuite(tests)
    else:
        return unittest.TestLoader().loadTestsFromTestCase(tests)
