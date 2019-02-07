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
DEFAULT_FORMATTER = u"%(levelname)s: %(message)s"
TIME_FORMATTER = u"%(levelname)s: %(asctime)s %(message)s"
CALLSITE_FORMATTER = u"%(levelname)s %(module)s..%(funcName)s: %(message)s"
CALLSITE_TIME_FORMATTER = u"%(levelname)s %(asctime)s %(module)s..%(funcName)s: %(message)s"


class AsynchRotatingFileHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super(AsynchRotatingFileHandler, self).__init__(*args, **kwargs)
        self._queue = Queue()
        self._thread = Thread(target=self._process)
        self._thread.daemon = True
        self._thread.start()

    def emit(self, record):
        self._queue.put(record)

    def _process(self):
        while True:
            super(AsynchRotatingFileHandler, self).emit(self._queue.get())

    def close(self):
        while not self._queue.empty():
            super(AsynchRotatingFileHandler, self).emit(self._queue.get())

        super(AsynchRotatingFileHandler, self).close()


def setup_logging(root_log_file, verbose, user_verbose, callsite=False, time=False):
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
        logger.removeHandler(handler)

