# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
The session module implements a higher order implementation for
communicating with the Pureport API.  The session module consumes the
`pureport.transport` module and provides session management
for communicating with the Pureport API.

This module exposes :class:`pureport.session.Session` class that is
responsible for handling the API session.  An instance of the
:class:`pureport.session.Session` class will automatically handle
authentication to the Pureport API using the credentials that are passed
at instatiation time.

To use this module, create an instance of :class:`pureport.session.Session`
and pass in a :class:`pureport.credentials.Credentials` instance.

.. code-block:: python

    from pureport.session import Session
    s = Session(credentials)
    s.get('/accounts')

If the session instance expires, it will automatically re-authorize using
the same passed credentials.
"""
from __future__ import absolute_import

import json
import time
import logging

from urllib.parse import urljoin

from pureport import defaults
from pureport.transport import Request

log = logging.getLogger(__name__)

__all__ = ('Session',)


class Session(Request):
    """
    "The `Session` object is responsible for building and managing
    a HTTP session using the underlying transport Request object.  The
    session provides a number of convience methods for sending
    requests to the remote server and is responsible for handling
    authorization using the provided credentials
    """

    def __init__(self, credentials, base_url=None):
        """Initializes a new instance of `Session`

        :param credentials: credentials object to use to authorize
            the session with the Pureport API
        :type credentials: :class:`pureport.credentials.Credentials`

        :param base_url: sets the base URL to use when making requests
            of the Pureport API.  This value typically does not need
            to be configured.
        :type base_url: string

        :returns: an instance of `Session`
        :rtype: :class:`pureport.session.Session`
        """
        self.credentials = credentials

        self.authorization_header = None
        self.authorization_expiration = None

        self.base_url = base_url or defaults.api_base_url

        super(Session, self).__init__()

    @property
    def authorized(self):
        """Returns whether or not current session is authorized

        :return: session authorization state
        :rtype: bool
        """
        if self.authorization_header is not None:
            if self.authorization_expiration >= time.time():
                return True
        return False

    def __call__(self, method, url, body=None, headers=None, query=None):
        """Manages the sending and receiving of requests

        This method provides some additional capabilities built
        on top of the :class:`pureport.transport.Request` instance.
        Namely this method will ensure the session is authorized and
        attempt to authorize to the API if it isn't.

        :param method: The HTTP method to call
        :type method: string

        :param url: The HTTP url to send the request to.  The URL
            parameter should be relative to the base url that was
            provided when the session was established
        :type url: string

        :param body: The string to include in the HTTP body
        :type body: string

        :param headers: Key/value pairs to be included in the request
            HTTP headers
        :type headers: dict

        :param query: Key/value pairs used to construct the query string
        :type query: dict

        :return: Instance of Response
        :rtype: :class:`pureport.transport.Response`
        """
        log.debug("creating {} request for {}".format(method, url))

        if not self.authorized:
            log.debug("session not authorized, attempting authorization")
            self.authorize()
            log.debug("session authorized successfully")

        headers = headers or {}
        headers.update(self.authorization_header)
        headers.update({'Content-Type': 'application/json'})

        if isinstance(body, dict):
            body = json.dumps(body)

        url = urljoin(self.base_url, url)

        log.debug("sending request to {}".format(self.base_url))
        log.debug("body={}".format(body))
        resp = super(Session, self).__call__(method, url, body, headers, query=query)
        log.debug("received valid response, returning to calling function")
        return resp

    def authorize(self):
        """Handles authorizing the session against the Pureport API

        This method will attempt to authorize the session using
        the provided credentials.  Typically this method is
        automatically called by the instance of `Session` and you
        should not need to invoke it directly.
        """
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(self.credentials._asdict())

        url = urljoin(self.base_url, '/login')

        resp = super(Session, self).__call__(
            'POST', url, body=body, headers=headers
        )

        data = json.loads(resp.data)

        self.authorization_header = {
            'Authorization': 'Bearer {access_token}'.format(**data)
        }

        self.authorization_expiration = time.time() + data['expires_in']

    def get(self, url, body=None, headers=None, query=None):
        """ HTTP GET method

        :param url: Fully qualified HTTP URL
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: Optional HTTP headers
        :type headers: dict

        :param query: Optional HTTP query string
        :type field: dict

        :return: HTTP Response object
        :rtype: :class:`pureport.transport.Response`
        """
        return self.__call__('GET', url, body=body, headers=headers, query=query)

    def post(self, url, body=None, headers=None, query=None):
        """ HTTP POST method

        :param url: Fully qualified HTTP URL
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: Optional HTTP headers
        :type headers: dict

        :param query: Optional HTTP query string
        :type field: dict

        :return: HTTP Response object
        :rtype: :class:`pureport.transport.Response`
        """
        return self.__call__('POST', url, body=body, headers=headers, query=query)

    def put(self, url, body=None, headers=None, query=None):
        """ HTTP PUT method

        :param url: Fully qualified HTTP URL
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: Optional HTTP headers
        :type headers: dict

        :param query: Optional HTTP query string
        :type field: dict

        :return: HTTP Response object
        :rtype: :class:`pureport.transport.Response`
        """
        return self.__call__('PUT', url, body=body, headers=headers, query=query)

    def delete(self, url, body=None, headers=None, query=None):
        """ HTTP DELETE method

        :param url: Fully qualified HTTP URL
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: Optional HTTP headers
        :type headers: dict

        :param query: Optional HTTP query string
        :type query: dict

        :return: HTTP Response object
        :rtype: :class:`pureport.transport.Response`
        """
        return self.__call__('DELETE', url, body=body, headers=headers, query=query)

    def options(self, url, body=None, headers=None):
        """ HTTP OPTIONS method

        :param url: Fully qualified HTTP URL
        :type url: string

        :param body: HTTP payload
        :type body: string

        :param headers: Optional HTTP headers
        :type headers: dict

        :return: HTTP Response object
        :rtype: :class:`pureport.transport.Response`
        """
        return self.__call__('OPTIONS', url, body=body, headers=headers)
