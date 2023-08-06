# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import json
import time

from functools import partial
from unittest.mock import patch
from collections import namedtuple

import pureport.session

from ..utils import utils


SentinelResponse = namedtuple('SentinelResponse', ('status', 'data', 'headers'))
response = partial(SentinelResponse, status=200, data=None, headers=None)

urllib3 = pureport.transport.urllib3.PoolManager

authorization = {'Authorization': utils.random_string()}

credentials = namedtuple('Credentials', ('key', 'secret'))(
        utils.random_string(), utils.random_string()
)


@patch.object(urllib3, 'request')
def test_call(mock_request):
    mock_request.return_value = response()

    s = pureport.session.Session(credentials)
    s.authorization_header = authorization
    s.authorization_expiration = time.time() + 3600

    url = utils.random_string()
    headers = {'Content-Type': 'application/json'}
    headers.update(authorization)

    resp = s('GET', url)

    assert resp.status == 200
    assert resp.data is None
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_convenience_methods(mock_request):
    mock_request.return_value = response()

    s = pureport.session.Session(credentials)
    s.authorization_header = authorization
    s.authorization_expiration = time.time() + 3600

    url = utils.random_string()
    headers = {'Content-Type': 'application/json'}
    headers.update(authorization)

    for item in ('get', 'post', 'put', 'delete', 'options'):
        resp = getattr(s, item)(url)

        assert resp.status == 200
        assert resp.data is None
        assert resp.json is None


@patch.object(urllib3, 'request')
def test_call_converts_dict_to_json(mock_request):
    mock_request.return_value = response()

    s = pureport.session.Session(credentials)
    s.authorization_header = authorization
    s.authorization_expiration = time.time() + 3600

    url = utils.random_string()

    resp = s(
        method='post',
        url=url,
        body={utils.random_string(): utils.random_string()}
    )

    assert resp.status == 200
    assert resp.data is None
    assert resp.json is None


@patch.object(urllib3, 'request')
def test_call_with_authorize(mock_request):
    auth_response = {
        'access_token': utils.random_string(),
        'type': 'Bearer',
        'expires_in': time.time() + 3600
    }

    mock_request.return_value = response(data=json.dumps(auth_response))

    s = pureport.session.Session(credentials)
    url = utils.random_string()

    s('GET', url)

    assert s.authorization_header == {
        'Authorization': 'Bearer {}'.format(auth_response['access_token'])
    }
    assert s.authorization_expiration is not None
