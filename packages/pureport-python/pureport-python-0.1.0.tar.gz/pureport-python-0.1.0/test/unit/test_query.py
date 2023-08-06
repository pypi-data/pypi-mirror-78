# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

from collections import namedtuple

from unittest.mock import patch

import pytest

from ..utils import utils

from pureport import query
from pureport.exceptions import PureportError


Item = namedtuple('Item', ('id', 'name'))


def function():
    items = list()
    for i in range(0, 10):
        items.append(Item(i, 'item{}'.format(i)))
    return items


def test_find_object_by_id():
    resp = query.find_object(function, 5)
    assert resp.id == 5
    assert resp.name == 'item5'


def test_find_object_by_name():
    resp = query.find_object(function, 'item5')
    assert resp.id == 5
    assert resp.name == 'item5'


def test_find_object_raises_exception():
    with pytest.raises(PureportError):
        query.find_object(function, utils.random_string())


@patch.object(query, 'api')
def test_query_functions_exist(mock_api):
    mock_api.return_value = lambda: []

    query.make()

    assert hasattr(query, 'find_network')
    assert callable(query.find_network)
    assert hasattr(query, 'find_connection')
    assert callable(query.find_connection)
