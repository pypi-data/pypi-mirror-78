# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

"""
The credentials module handles loading, parsing and returning a valid
object that can be passed into a :class:`pureport.session.Session`
instance to authenticate to the Pureport API.  This module will search
for credentials in well-known locations as well as attempt to load
credentials from the current environment.

The method of precedence for credentials is:

    1) Environment
    2) Profile in ~/.pureport/credentials
    3) "default" profile in ~/.pureport/credentials

If no valid API key and/or API secret could be loaded, then a
:class:`pureport.exceptions.PureportError` exception is raised.
"""
from __future__ import absolute_import

import os
import json
import logging

from collections import namedtuple

import yaml

from pureport import defaults
from pureport.exceptions import PureportError


log = logging.getLogger(__name__)


__all__ = ('default',)


def default():
    """Attempts to discover the configured credentials

    This function will attempt to find the credentials to
    be used for authorizing a Pureport API session.  It will
    also discover the Pureport base API URL.  The function
    follows a strict order for loading crendentials.

    In order of precedence, the following credentials are used:

        1) Loaded from the current environment
        2) Loaded from ~/.pureport/credentials.[yml|yaml|json]

    The function will use the following environement variables:

        PUREPORT_API_KEY
        PUREPORT_API_SECRET
        PUREPORT_API_BASE_URL

    If the environment variables are not set, then this function
    will use the information in ~/.pureport/credentials.[yml|yaml|json].

    The credentials file will be used in the following order:

        1) ~/.pureport/credentials.yml
        2) ~/.pureport/credentials.yaml
        3) ~/.pureport/credentials.json

    The credentials file has the following structure:

    .. code-block:: yaml

        ---
        current_profile: <string, default='default'>
        profiles:
          <string>:
            api_url: <string>
            api_key: <string>
            api_secret: <string>


    If no valid credentials are able to be found, then the function will
    raise an exception.

    This function will return a tuple of two elements.  The first
    element will be a valid instance of
    :class:`pureport.credentials.Credentials`.  The second element will
    be a string that represents the Pureport API base url to
    use.  The tuple values can be used as the required arguments
    when creating a new instance of :class:`pureport.session.Session`.

    :return: a valid credentials instance, an api base url
    :rtype: tuple

    :raises: :class:`pureport.exceptions.PureportError`
    """
    file_path = defaults.credentials_path
    file_name = defaults.credentials_filename

    for ext in ('yml', 'yaml', 'json'):
        deserializer = json.loads if ext == 'json' else yaml.safe_load
        fp = os.path.join(file_path, '{}.{}'.format(file_name, ext))

        if os.path.exists(fp):
            with open(fp) as f:
                log.info("loading credentials file {}".format(fp))
                content = deserializer(f.read())
                break
    else:
        content = None
        values = {}

    if content:
        profile = content.get('current_profile', 'default')
        profiles = content.get('profiles', {})
        values = profiles.get(profile, profiles.get('default'))

    kwargs = {
        'key': defaults.api_key or values.get('api_key'),
        'secret': defaults.api_secret or values.get('api_secret')
    }

    base_url = defaults.api_base_url or values.get('api_url')

    if any((kwargs['key'] is None, kwargs['secret'] is None)):
        raise PureportError("missing or invalid credentials")

    return namedtuple('Credentials', kwargs)(**kwargs), base_url
