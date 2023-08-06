# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
This module provides a set of functions that responsible for
transforming data into a native Python data type.
"""
from __future__ import absolute_import

import re

from pureport.exceptions import PureportTransformError


def to_int(val):
    """Convert value to type int

    :param val: any valid object
    :type val: object

    :return: a int value
    :rtype: int

    :raises: :class:`pureport.exceptions.PureportTransformError`
    """
    try:
        return int(val)
    except ValueError as exc:
        raise PureportTransformError(
            "unable to convert value to type `int`",
            value=val,
            type=int,
            exc=exc
        )


def to_bool(val):
    """Convert value to type bool

    :param val: any valid object
    :type val: object

    :return: a bool value
    :rtype: bool
    """
    val = val.lower() if isinstance(val, str) else val

    # coerce the value to a true int.  this will happen if the
    # value came from the environment
    if isinstance(val, str):
        try:
            val = int(val)
        except ValueError:
            pass

    if isinstance(val, int):
        val = val != 0
    elif val in (True, 'true', '0'):
        val = True
    elif val in (False, 'false'):
        val = False
    elif isinstance(val, (list, dict, set, tuple)):
        val = len(val) != 0
    return bool(val)


def to_str(val):
    """Convert value to type str

    :param val: any valid object
    :type val: object

    :return: a str value
    :rtype: str
    """
    return str(val)


def to_float(val):
    """Convert value to type float

    :param val: any valid object
    :type val: object

    :return: a float value
    :rtype: float

    :raises: :class:`pureport.exceptions.PureportTransformError`
    """
    try:
        return float(val)
    except ValueError as exc:
        raise PureportTransformError(
            "uanble to convert value to type `float`",
            value=val,
            type=float,
            exc=exc
        )


def to_list(val):
    """Convert value to list

    :param val: any valid object
    :type val: object

    :return: a list object
    :rtype: list
    """
    if isinstance(val, (list, set, tuple, dict)):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


def to_snake_case(val):
    """Convert camel case to snake case

    :param val: string to convert to snake case
    :type val: str

    :return: a string in snake case
    :rtype: str
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', val)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
