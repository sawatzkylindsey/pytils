#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import pdb
from queue import Queue
from threading import Thread
import sys


USER = "user"
user_log = logging.getLogger(USER)
"""
A logger that outputs to standard out, suitable for user messaging.
"""
DEFAULT_FORMATTER = u"%(levelname)s: %(message)s"
TIME_FORMATTER = u"%(levelname)s: %(asctime)s %(message)s"
CALLSITE_FORMATTER = u"%(levelname)s %(module)s..%(funcName)s: %(message)s"
CALLSITE_TIME_FORMATTER = u"%(levelname)s %(asctime)s %(module)s..%(funcName)s: %(message)s"


class AsynchRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super(AsynchRotatingFileHandler, self).__init__(*args, **kwargs)
        self._queue = Queue()
        self._closed = False
        self._thread = Thread(target=self._process)
        # Not daemon threads to ensure that the program continues to run while there are still records that need to be logged.
        # As a result, callers must close this handler (ex: through @teardown below).
        self._thread.daemon = False
        self._thread.start()

    def emit(self, record):
        self._queue.put(record)

    def _process(self):
        while not self._closed:
            super(AsynchRotatingFileHandler, self).emit(self._queue.get())

    def close(self):
        self._closed = True

        while not self._queue.empty():
            super(AsynchRotatingFileHandler, self).emit(self._queue.get())

        super(AsynchRotatingFileHandler, self).close()


def setup_logging(root_log_file, verbose, user_verbose, callsite=False, time=False):
    """Initialize the pytil's logger.

    .. note: be sure to use with log.teardown

    >>> @teardown
    >>> def main(..):
    >>>     setup_logging(".%s.log" % os.path.splitext(os.path.basename(__file__))[0], aargs.verbose, False)
    >>>     ..

    :param root_log_file: the log file, commonly declared as '".%s.log" % os.path.splitext(os.path.basename(__file__))[0]'
    :type function: str
    :param verbose: use the DEBUG logging level in the root logger
    :type verbose: bool
    :param user_verbose: use the DEBUG logging level in the user_log
    :type user_verbose: bool
    :param callsite: configure the log formatter to include the callsite in the form 'module..function'
    :type callsite: bool
    :param time: configure the log formatter to include time
    :type time: bool
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    if user_verbose:
        user_log.setLevel(logging.DEBUG)
    else:
        user_log.setLevel(logging.INFO)

    #                                                                       5MBs
    root_handler = AsynchRotatingFileHandler(root_log_file, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    root_handler.setFormatter(_get_formatter(callsite, time))
    _clear_handlers(logging.getLogger())
    logging.getLogger().addHandler(root_handler)
    logging.debug("setup_logging(f=%s, v=%s, uv=%s, c=%s, t=%s)" % (root_log_file, verbose, user_verbose, callsite, time))

    user_handler = logging.StreamHandler(sys.stdout)
    user_handler.setFormatter(logging.Formatter("%(message)s"))
    _clear_handlers(user_log)
    user_log.addHandler(user_handler)


def teardown(function):
    """Decorator to ensure the logging handlers are closed on exit.

    .. note: be sure to use with log.setup_logging

    >>> @teardown
    >>> def main(..):
    >>>     setup_logging(..)
    >>>     ..

    :param function: the function to decorate
    :type function: function
    """
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        finally:
            _clear_handlers(logging.getLogger())

    return wrapper


def _get_formatter(callsite, time):
    if callsite and time:
        return logging.Formatter(CALLSITE_TIME_FORMATTER)
    elif callsite:
        return logging.Formatter(CALLSITE_FORMATTER)
    elif time:
        return logging.Formatter(TIME_FORMATTER)
    else:
        return logging.Formatter(DEFAULT_FORMATTER)


def _clear_handlers(logger):
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

