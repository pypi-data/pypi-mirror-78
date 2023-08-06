# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
The api module dynamically loads and binds a set of Python functions
based on the Pureport OpenAPI specification.  This module will
creates an instance of `pureport.session.Session`, authenticates using
the `pureport.credentials` module and downloads the OpenAPI
specification from the Pureport API.

The module will create callable Python functions that coorespond to
the `operationId` and HTTP method found in the Pureport OpenAPI
specification.

.. note::
    All values extracted from the Pureport OpenAPI specification
    have been converted from camel case to snake case.  For instance
    to use the `findNetworks` function, it would be invoked by
    issuing `find_networks`.

To use this module, simply import it into your code and call the
appropriate function.

For example, to find all networks associated with the authenticated
account:

    .. code-block:: python

        import pureport.api
        networks = pureport.api.find_networks()

All function responses will be returned as `pureport.models.Model`
objects.  Please see `pureport.models` for more details.
"""
from __future__ import absolute_import

import json
import logging

from functools import (
    partial,
    update_wrapper,
)


from pureport.transforms import (
    to_list,
    to_snake_case
)

from pureport import (
    models,
    defaults
)

from pureport.helpers import (
    get_api,
    get_value
)

from pureport.session import Session
from pureport.credentials import default
from pureport.exceptions import PureportError


log = logging.getLogger(__name__)


def send_request(session, url, method='GET', status_codes=None, variables=None, query=None, **kwargs):
    """Sends a request to the Pureport REST API

    This function will invoke a HTTP method when calling the
    Pureport API and return the response.  Any kwargs provided
    will be converted to JSON and included as the body of the
    request

    :param method: The HTTP method to call
    :type method: string

    :param url: The HTTP realitive URL to invoke
    :type url: string

    :param kwargs: Unordered key/value pair to be included in
        request as a JSON payload
    :type kwargs: dict

    :returns: The HTTP response from the server
    :rtype: :class:`pureport.transport.Response`
    """
    status_codes = to_list(status_codes) or (200,)

    body = json.dumps(kwargs.get('body', {})) if kwargs else None
    url = url.format(**(variables or {}))

    log.debug("calling session with url {}".format(url))
    response = session(method, url, body=body, query=query)

    if response.status not in status_codes:
        raise PureportError("invalid status code received from response")

    assert hasattr(response, 'json'), "missing required attribute `json`"

    return response.json


get = partial(send_request, method='GET', status_codes=(200,))
update_wrapper(get, send_request)

put = partial(send_request, method='PUT', status_codes=(200,))
update_wrapper(put, send_request)

post = partial(send_request, method='POST', status_codes=(201,))
update_wrapper(post, send_request)

delete = partial(send_request, method='DELETE', status_codes=(200,))
update_wrapper(delete, send_request)


def request(session, method, uri, *args, **kwargs):
    """Send a request to the URI and return the response

    :param method: the http method to call
    :type method: str

    :param uri: the relative uri to call
    :type: uri: str
    """
    api = get_api(session)

    method = method.lower()
    path = api['paths'][uri].get(method)

    if path is None:
        raise PureportError("method {} not supported for uri {}".format(method, uri))

    parameters = list()
    query = {}
    for item in path.get('parameters', []):
        if item.get('in', 'path') == 'path' and item.get('required', True) is True:
            parameters.append(item['name'])
        elif item.get('in') == 'query':
            query[to_snake_case(item['name'])] = None

    cls = None

    ref = get_value('requestBody.content.application/json.schema.$ref', path)
    if ref:
        clsname = ref.split('/')[-1]
        schema = getattr(models, clsname)._schema

        if schema.discriminator:
            propval = getattr(args[1], schema.discriminator['propertyName'])
            clsname = schema.discriminator['mapping'].get(propval).split('/')[-1]

        cls = getattr(models, clsname, None)
        log.debug("connection class is {}".format(cls))
        parameters.append('model')

    query_values = kwargs.pop('query', None)
    if query_values:
        # TODO need to validate query inputs against api spec
        if not set(query_values).issubset(query):
            raise PureportError("unknown query value provided")

    variables = dict(zip(parameters, args))

    for item in parameters:
        if item not in variables:
            variables[item] = kwargs.pop(to_snake_case(item), None)

    model = variables.get('model')

    body = None

    if cls and isinstance(model, cls):
        body = models.dump(model)

    if kwargs:
        raise PureportError("unexpected keyword arguments")

    if set(args).issubset(variables.values()) is False:
        raise PureportError("unexpected positional arguments")

    for p in parameters:
        if variables.get(p) is None:
            raise PureportError("missing required argument: {}".format(to_snake_case(p)))

    func = globals().get(method)
    data = func(session, uri, body=body, variables=variables, query=query_values)

    schema = get_value('responses.default.content.application/json.schema', path)
    if schema:
        if '$ref' in schema:
            clsname = schema['$ref'].split('/')[-1]
        elif schema.get('type') == 'array' and 'items' in schema:
            clsname = schema['items']['$ref'].split('/')[-1]

        if isinstance(data, list):
            data = [models.load(clsname, item) for item in data]
        else:
            data = models.load(clsname, data)

    return data


def make():
    log.debug("attempting to make bindings for openapi spec")

    session = Session(*default())
    apispec = get_api(session)

    models.make(apispec)

    for uri, properties in apispec['paths'].items():
        for method, attrs in properties.items():
            if 'operationId' in attrs:
                name = to_snake_case(attrs['operationId'])
                func = partial(request, session, method, uri)
                func.__doc__ = attrs.get('summary')
                func.__name__ = name
                log.debug('adding function {}'.format(name))
                globals()[name] = func


if defaults.automake_bindings is True:
    make()
