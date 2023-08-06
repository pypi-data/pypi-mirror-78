# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import logging

from logging import NullHandler, StreamHandler

import pureport


def test_descriptors_are_present():

    assert pureport.__version__ is not None
    assert pureport.__author__ == 'Pureport, Inc'
    assert pureport.__license__ == 'MIT'


def test_global_logging_settings():
    assert pureport.logging.disable_existing_loggers is False

    log = logging.getLogger('pureport')
    assert log.level == 0

    for handler in log.handlers:
        if isinstance(handler, NullHandler):
            break
    else:
        raise Exception("log 'pureport' is missing NullHandler")


def test_set_logging():
    log = logging.getLogger('pureport')

    assert log.level == 0

    pureport.set_logging(10)

    for handler in log.handlers:
        if isinstance(handler, StreamHandler):
            break
    else:
        raise Exception("log 'pureport' is missing StreamHandler")

    assert log.level == 10

    pureport.set_logging(0)

    assert log.level == 0
