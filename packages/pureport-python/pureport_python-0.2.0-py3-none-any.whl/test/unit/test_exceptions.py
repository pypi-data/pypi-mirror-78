# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from unittest.mock import MagicMock

import pureport.exceptions as exceptions

from ..utils import utils


def test_pureport_error():
    message = utils.random_string()
    obj = MagicMock()

    exc = exceptions.PureportError(message, exc=obj)

    assert exc.message == message
    assert exc.exc == obj


def test_pureport_transport_error():
    message = utils.random_string()
    obj = MagicMock()

    exc = exceptions.PureportTransportError(message, exc=obj)

    assert exc.message == message
    assert exc.exc == obj


def test_pureport_http_error():
    message = utils.random_string()
    status = utils.random_string()
    code = utils.random_string()

    response = MagicMock(json={
        'status': status,
        'code': code,
        'message': message
    })

    exc = exceptions.PureportHttpError(response)

    assert exc.message == message
    assert exc.status == status
    assert exc.code == code


def test_pureport_transform_error():
    message = utils.random_string()
    value = utils.random_string()
    type = utils.random_string()
    exc = utils.random_string()

    obj = exceptions.PureportTransformError(message, value, type, exc)

    assert obj.message == message
    assert obj.value == value
    assert obj.type == type
    assert obj.exc == exc
