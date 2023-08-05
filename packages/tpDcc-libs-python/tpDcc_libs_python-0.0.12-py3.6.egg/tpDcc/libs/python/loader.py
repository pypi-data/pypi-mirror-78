#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDcc-libs-python
"""

from __future__ import print_function, division, absolute_import

import os
import logging.config

# =================================================================================

PACKAGE = 'tpDcc.libs.python'

# =================================================================================


def init(dev=False):
    """
    Initializes tpDcc.libs.python package
    :param dev: bool, Whether tpDcc-libs-python is initialized in dev mode or not
    :return: bool
    """

    from tpDcc.libs.python import register

    if dev:
        register.cleanup()

    # importer.init_importer(package=PACKAGE)

    logger = create_logger(dev=dev)
    register.register_class('logger', logger)


def create_logger(dev=False):
    """
    Creates logger for current tpDcc-libs-python package
    """

    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)

    logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))

    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
    logger = logging.getLogger('tpDcc-libs-python')
    if dev:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    return logger
