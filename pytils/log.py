#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
import sys

USER = "user"
user_log = logging.getLogger(USER)
DEFAULT_FORMATTER = u"%(levelname)s: %(message)s"
CALLSITE_FORMATTER = u"%(levelname)s %(module)s..%(funcName)s: %(message)s"

def setup_logging(root_log_file, verbose, callsite=False):
    logging.getLogger().setLevel(logging.DEBUG)

    if verbose:
        user_log.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        user_log.setLevel(logging.INFO)
        logging.getLogger().setLevel(logging.INFO)

    #                                                                  5MBs
    root_handler = RotatingFileHandler(root_log_file, maxBytes=5*1024*1024, backupCount=5, encoding="utf-8")
    root_handler.setFormatter(logging.Formatter(CALLSITE_FORMATTER if callsite else DEFAULT_FORMATTER))
    logging.getLogger().addHandler(root_handler)

    user_handler = logging.StreamHandler(sys.stdout)
    user_handler.setFormatter(logging.Formatter("%(message)s"))
    user_log.addHandler(user_handler)

