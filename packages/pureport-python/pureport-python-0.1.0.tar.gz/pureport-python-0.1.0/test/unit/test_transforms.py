# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import pytest

import pureport.transforms as transforms
from pureport.exceptions import PureportTransformError

from ..utils import utils


def test_to_int():
    for item in (utils.random_int(), str(utils.random_int())):
        resp = transforms.to_int(item)
        assert isinstance(resp, int)


def test_to_int_exc():
    with pytest.raises(PureportTransformError):
        transforms.to_int(utils.random_string())


def test_to_bool():
    for item in (True, 'TRUE', 'True', 1, 10, utils.random_string()):
        resp = transforms.to_bool(item)
        assert resp is True, item

    for item in (False, 'FALSE', 'False', 0, '', None):
        resp = transforms.to_bool(item)
        assert resp is False, item

    for item in ({}, [], ()):
        resp = transforms.to_bool(item)
        assert resp is False, item

    items = (
        {utils.random_string(): utils.random_string()},
        [utils.random_string()],
        (utils.random_string,)
    )

    for item in items:
        resp = transforms.to_bool(item)
        assert resp is True, item


def test_to_str():
    for item in (True, False, utils.random_int(), utils.random_string()):
        resp = transforms.to_str(item)
        assert isinstance(resp, str)


def test_to_float():
    for item in (utils.random_float(), utils.random_int()):
        resp = transforms.to_float(item)
        assert isinstance(resp, float)


def test_to_float_exc():
    with pytest.raises(PureportTransformError):
        transforms.to_float(utils.random_string())


def test_to_list():
    numbers = list()
    for x in range(0, 10):
        numbers.append(utils.random_int())

    string = utils.random_string()

    obj = dict([(n, string) for n in numbers])

    result = transforms.to_list(set(numbers))
    assert sorted(result) == sorted(list(set(numbers)))

    result = transforms.to_list(tuple(numbers))
    assert sorted(result) == sorted(numbers)

    result = transforms.to_list(numbers)
    assert sorted(result) == sorted(numbers)
    assert id(result) != id(numbers)

    result = transforms.to_list(obj)
    assert sorted(result) == sorted(obj.keys())

    result = transforms.to_list(string)
    assert result == [string]

    result = transforms.to_list(None)
    assert result == []


def test_to_snake_case():
    strings = list()
    for x in range(0, 5):
        strings.append(utils.random_string(True))

    test_string = "".join([s.title() for s in strings])
    expected_string = "_".join([s.lower() for s in strings])

    assert transforms.to_snake_case(test_string) == expected_string
