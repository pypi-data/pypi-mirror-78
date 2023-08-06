# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
This module contains all of the Pureport Python exception classes
that are used in this project.  All exceptions derive from the base
class :class:`pureport.exceptions.PureportError`.
"""
from __future__ import absolute_import


class PureportError(Exception):
    """
    The base class for all exceptions raised from the Pureport Python
    SDK code.  All SDK exceptions raised from this SDK are derived
    from this base class.

    .. code-block:: python

        from pureport.exceptions import PureportError
        raise PureportError("error message here")

    """

    def __init__(self, message, exc=None):
        super(PureportError, self).__init__(message)
        self._message = message
        self._exc = exc

    @property
    def message(self):
        return self._message

    @property
    def exc(self):
        return self._exc


class PureportTransportError(PureportError):
    """
    An exception is raised from `pureport.transport` that
    indicates there was an error attempting to handle the communication
    to or from the remote server.   This exception class is the base
    exception class for all transport exceptions and is derived from
    :class:`PureportError`
    """

    def __init__(self, message, exc=None):
        super(PureportTransportError, self).__init__(message, exc)


class PureportTransformError(PureportError):
    """
    This exception class is raised when trying to coerce a value
    from one type to another type.  The resulting exception
    provides access to the original value, the requested value
    type and the inner exception raised by the transform.
    """
    def __init__(self, message, value, type, exc):
        super(PureportTransformError, self).__init__(message, exc)
        self.value = value
        self.type = type


class PureportHttpError(PureportTransportError):
    """
    An exception raised from introspecting the HTTP status code in
    a valid HTTP response.  This error indicates the transmission to
    and from the remote server are fine but there is an error in
    the server's ability to process the payload and/or the destination
    URL

    This exception class takes a single argument that is the HTTP
    response and parses the data for the exception.

    .. code-block:: python

        from pureport.exceptions import PureportHttpError
        raise PureportHttpError(response)

    The response object should be an instance of
    :class:`pureport.transport.Response`
    """

    def __init__(self, response):
        """Initialize the exception class

        :param response: A HTTP Response instance
        :param type: :class:`pureport.transport.Response`

        :return: An exception class that represents the HTTP error
        :rtype: :class:`pureport.exceptions.PureportHttpError`
        """
        super(PureportHttpError, self).__init__(response.json.get('message'))
        self._response = response

    @property
    def status(self):
        """The HTTP status code returned from the remote server

        :return: HTTP status
        :rtype: int
        """
        return self._response.json.get('status')

    @property
    def code(self):
        """The HTTP text code returned from the remote server

        :return: HTTP code
        :rtype: string
        """
        return self._response.json.get('code')

    @property
    def message(self):
        """The HTTP message returned from the remote server

        :return: HTTP message
        :rtype: string
        """
        return self._response.json.get('message')
