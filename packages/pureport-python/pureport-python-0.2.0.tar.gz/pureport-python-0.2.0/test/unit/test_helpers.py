# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import json

from unittest.mock import patch, MagicMock
from collections import namedtuple
from functools import partial

import pytest

from pureport import helpers
from pureport.exceptions import PureportError

from ..utils import utils

SentinelResponse = namedtuple('SentinelResponse', ('status', 'data', 'headers', 'json'))
response = partial(SentinelResponse, status=200, data=None, headers=None, json=None)


@patch('builtins.print')
def test_print_reponse(mock_print):

    class Response(object):
        json = utils.random_string()

    response = Response()
    helpers.print_response(response)
    mock_print.assert_called_with(
        json.dumps(response.json, indent=4, sort_keys=True)
    )


@patch('builtins.print')
def test_print_json(mock_print):
    obj = {utils.random_string(): utils.random_string()}
    helpers.print_json(obj)
    mock_print.assert_called_with(
        json.dumps(obj, indent=4, sort_keys=True)
    )


def test_first():
    items = list()
    for x in range(0, utils.random_int()):
        items.append(x)

    text = utils.random_string()

    assert helpers.first(items) == items[0]
    assert helpers.first([]) == []
    assert helpers.first(None) is None
    assert helpers.first(text) == text


def test_get_api():
    mock_session = MagicMock()
    mock_session.return_value = response(status=400)
    with pytest.raises(PureportError):
        helpers.get_api(mock_session)


def test_get_value():
    parent = utils.random_string()

    child1 = utils.random_string()
    subchild1 = utils.random_string()
    value1 = utils.random_string()

    child2 = utils.random_string()
    subchild2 = utils.random_string()
    value2 = utils.random_string()

    child3 = utils.random_string()
    items = [utils.random_string for x in range(0, 11)]

    obj = {
        parent: {
            child1: {
                subchild1: value1
            },
            child2: {
                subchild2: value2
            },
            child3: items
        }
    }

    path = ".".join((parent, child2, subchild2))
    assert helpers.get_value(path, obj) == value2

    path = ".".join((parent, child3, str(1)))
    assert helpers.get_value(path, obj) == items[1]

    path = "invalid.path"
    assert helpers.get_value(path, obj) is None
