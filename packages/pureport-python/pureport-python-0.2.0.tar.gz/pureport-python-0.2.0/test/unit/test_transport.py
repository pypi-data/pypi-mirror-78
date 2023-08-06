# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import json

from functools import partial
from unittest.mock import patch
from collections import namedtuple

import pytest

import pureport.transport

from pureport.exceptions import PureportHttpError
from pureport.exceptions import PureportTransportError

from ..utils import utils


SentinelResponse = namedtuple('SentinelResponse', ('status', 'data', 'headers'))
response = partial(SentinelResponse, status=200, data=None, headers=None)

urllib3 = pureport.transport.urllib3.PoolManager


@patch.object(urllib3, 'request')
def test_default(mock_request):
    mock_request.return_value = response()
    req = pureport.transport.Request()
    url = utils.random_string()
    resp = req('GET', url)
    mock_request.assert_called_with('GET', url, body=None, headers=None, fields=None)
    assert resp.status == 200
    assert resp.data is None
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_methods_with_body(mock_request):
    mock_request.return_value = response()
    req = pureport.transport.Request()
    data = {utils.random_string(): utils.random_string()}
    url = utils.random_string()
    resp = req('GET', url, data)
    mock_request.assert_called_with('GET', url, body=data, headers=None, fields=None)
    assert resp.status == 200
    assert resp.data is None
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_methods_return_data(mock_request):
    response_data = str((utils.random_string(), utils.random_string(), utils.random_string()))
    mock_request.return_value = response(data=response_data)
    req = pureport.transport.Request()
    data = {utils.random_string(): utils.random_string()}
    url = utils.random_string()
    resp = req('GET', url, data)
    mock_request.assert_called_with('GET', url, body=data, headers=None, fields=None)
    assert resp.status == 200
    assert resp.data == response_data
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_methods_return_data_and_json(mock_request):
    response_data = json.dumps({utils.random_string(): utils.random_string()})
    mock_request.return_value = response(data=response_data)
    req = pureport.transport.Request()
    data = {utils.random_string(): utils.random_string()}
    url = utils.random_string()
    resp = req('GET', url, body=data)
    mock_request.assert_called_with('GET', url, body=data, headers=None, fields=None)
    assert resp.status == 200
    assert resp.data == response_data
    assert resp.json == json.loads(response_data)


@patch.object(urllib3, 'request')
def test_response(mock_request):
    resp = pureport.transport.Response(response())
    assert resp.status == 200
    assert resp.data is None
    assert resp.headers is None
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_response_is_immutable(mock_request):
    resp = pureport.transport.Response(None)
    for item in ('status', 'data', 'headers', 'json'):
        with pytest.raises(AttributeError):
            setattr(resp, item, utils.random_string())


@patch.object(urllib3, 'request')
def test_http_exception(mock_request):
    error = {'status': 400, 'code': 'ERROR', 'message': utils.random_string()}
    mock_request.return_value = response(status=400, data=json.dumps(error))
    req = pureport.transport.Request()
    with pytest.raises(PureportHttpError):
        req('GET', utils.random_string())


def test_bad_url():
    with pytest.raises(PureportTransportError):
        req = pureport.transport.Request()
        req('GET', utils.random_string())
