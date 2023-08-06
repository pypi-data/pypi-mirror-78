# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import os
import re
import json

from functools import partial
from collections import namedtuple
from unittest.mock import patch, MagicMock

from pureport import api

SentinelResponse = namedtuple('SentinelResponse', ('status', 'data', 'headers', 'json'))
response = partial(SentinelResponse, status=200, data=None, headers=None, json=None)


def generate_response(method, url, body=None, headers=None, query=None):
    if url == '/openapi.json':
        basepath = os.path.dirname(__file__)
        content = open(os.path.join(basepath, '../openapi.json')).read()
        return response(data=content, json=json.loads(content))

    elif url == '/accounts':
        return response(data=json.dumps([]), json=[])


@patch.object(api, 'Session')
def test_api_methods_exist(mock_session):
    basepath = os.path.dirname(__file__)
    content = open(os.path.join(basepath, '../openapi.json')).read()
    mock_session.get.return_value = content

    methods = re.findall('operationId: (.+)', content, re.M)
    assert set(methods).issubset(dir(api))


def test_request():
    mock_session = MagicMock()

    mock_session.side_effect = partial(generate_response)
    mock_session.get.side_effect = partial(generate_response, 'GET')

    api.request(mock_session, 'GET', '/accounts')


@patch.object(api, 'get_api')
def test_make(mock_get_api):
    basepath = os.path.dirname(__file__)
    content = open(os.path.join(basepath, '../openapi.json')).read()
    mock_get_api.return_value = json.loads(content)

    api.make()

    methods = re.findall('operationId: (.+)', content, re.M)
    assert set(methods).issubset(dir(api))
