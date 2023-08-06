# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
Pureport Python Client

The Pureport Python client provides an implementation in Python for
consuming the Pureport Fabric API.  It is designed to provide a
set of bindings for calling the Fabric API REST endpoints and
is responsible for handling session setup, authorization, transport
and logging.

In order to get started using the Pureport Python client, you must first
have a valid Pureport account and configure an API key.  Once you
have your API key and API secret, set the following environment
variables:

    .. code-block:: bash

        export PUREPORT_API_KEY=<your api key>
        export PUREPORT_API_SECRET=<your api secret>

Once the environment variable are set, the Pureport Python client will
automatically read the values when you create a new instance of
:class:`pureport.session.Session`.

    .. code-block:: python

        from pureport.session import Session
        from pureport.credentials import default

        session = Session(*default())
        session.get('/accounts')

The code block example above will create an instance of `Session` and
load the default credentials.

All logging is turned off by default.  The Pureport module provides
a convenience function to enable logging.  To use the function, simply
import the module and set the desired logging level.

    .. code-block:: python

        import pureport
        pureport.set_logging(10)

The Pureport Python client also provides automatic bindings for the
Pureport OpenAPI specification.  For additional information please
see the `pureport.api` module.
"""
from __future__ import absolute_import

import logging

from logging import NullHandler

from pureport import defaults


__version__ = "0.2.0"

__author__ = "Pureport, Inc"
__license__ = "MIT"

logging.disable_existing_loggers = False

logging.getLogger(__name__).addHandler(NullHandler())
logging.getLogger(__name__).setLevel(logging.NOTSET)


def set_logging(level):
    """Convenience function to enable logging for the SDK

    This function will enable logging for the SDK at the level
    provided.  It sends all logging information to stderr.

    :param level: logging level to emit
    :type level: int
    """
    log = logging.getLogger(__name__)
    log.setLevel(level)

    for handler in log.handlers:
        if handler.get_name() == __name__:
            log.debug("logging handler {} is already configured".format(handler.get_name()))
            break

    else:
        handler = logging.StreamHandler()
        handler.set_name(__name__)
        handler.setFormatter(logging.Formatter("%(asctime)s: %(name)s: %(message)s"))
        log.addHandler(handler)
        log.debug("Added stderr logging handler to logger: %s", __name__)


set_logging(defaults.logging_level)
