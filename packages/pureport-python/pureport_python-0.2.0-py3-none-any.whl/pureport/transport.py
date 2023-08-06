# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
This module provides the low level implementation for sending and
receiving data from the Pureport API.  This module is mostly a wrapper
around the urllib3 library.  It exposes two primary classes for
handling requests and responses.

This module should be considered mostly an internal module and should
not be used directly outside the SDK generally speaking.  The Pureport
Python SDK provides a high level implementation for interfacing with
the Pureport API.  See `pureport.session` for more details.
"""
from __future__ import absolute_import

import json
import logging

import urllib3

from urllib3.exceptions import HTTPError
from urllib3.exceptions import TimeoutError

from pureport import defaults
from pureport.exceptions import PureportTransportError
from pureport.exceptions import PureportHttpError


log = logging.getLogger(__name__)

__all__ = ('Request', 'Response')


class Response(object):
    """
    The Response object returns the HTTP Response
    """

    def __init__(self, response):
        self._response = response

    @property
    def status(self):
        """Returns the HTTP status code

        :return: HTTP status code
        :rtype: int
        """
        return self._response.status

    @property
    def data(self):
        """Returns the HTTP payload

        :return: HTTP data payload
        :rtype: string
        """
        return self._response.data

    @property
    def headers(self):
        """Returns the HTTP headers

        :return: HTTP headers
        :rtype: dict
        """
        return self._response.headers

    @property
    def json(self):
        """Returns the HTTP JSON data

        :return: HTTP JSON data
        :rtype: dict
        """
        try:
            return json.loads(self._response.data)
        except Exception:
            pass


class Request(object):
    """
    The Request object provides an interface for making HTTPS requests

    This interface handles sending the HTTPS request to the provided
    URL for a given method and will return an instance of
    :class:`Response`
    """

    def __init__(self, connect_timeout=None, read_timeout=None):
        """Initialize a new `Request` instance

        :param connect_timeout: HTTP connect timeout (default=3.0)
        :type connect_timeout: float

        :param read_timeout: HTTP read timeout (default=10.0)
        :type read_timeout: float

        :return: HTTP Request object
        :rtype: :class:`Request`
        """
        connect_timeout = defaults.transport_connect_timeout
        read_timeout = defaults.transport_read_timeout
        self.http = urllib3.PoolManager(
            headers={'Content-Type': 'application/json'},
            timeout=urllib3.util.Timeout(connect_timeout, read_timeout)
        )
        log.debug(
            "Created new HTTP Pool (connect_timeout={}, "
            "read_timeout={})".format(connect_timeout, read_timeout)
        )

    def __call__(self, method, url, body=None, headers=None, query=None):
        """Sends the HTTP request

        :param method: HTTP method
        :type method: string

        :param url: HTTP URI
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: HTTP headers
        :type headers: dict

        :param query: HTTP query string
        :type query: dict

        :return: HTTP Response
        :rtype: :class:`Response`
        """
        try:
            log.debug("Sending request to remote server")
            log.debug("method={}, url={}".format(method, url))
            log.debug("headers={}".format(','.join(headers or {})))
            resp = self.http.request(method, url, body=body, headers=headers, fields=query)
        except (HTTPError, TimeoutError) as exc:
            message = getattr(exc, 'message', None) or \
                    defaults.generic_transport_error_message
            raise PureportTransportError(message, exc=exc)

        log.debug("Received response from remote server")
        log.debug("HTTP status code {}".format(resp.status))
        log.debug("HTTP headers={}".format(','.join(headers or {})))

        resp = Response(resp)

        if resp.status >= 400:
            raise PureportHttpError(resp)

        return resp
