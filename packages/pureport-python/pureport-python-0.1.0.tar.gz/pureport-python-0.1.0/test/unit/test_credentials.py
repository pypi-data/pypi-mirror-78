# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import os
import json

from unittest.mock import patch

import pytest

import yaml

import pureport.credentials as credentials
from pureport.exceptions import PureportError

from ..utils import utils


@patch.object(credentials, 'defaults')
def test_load_from_environment(mock_defaults):
    api_key = utils.random_string()
    api_secret = utils.random_string()
    api_url = utils.random_string()

    with utils.tempdir() as tmpdir:
        mock_defaults.credentials_path = tmpdir
        mock_defaults.credentials_filename = 'credentials'

    mock_defaults.api_key = api_key
    mock_defaults.api_secret = api_secret
    mock_defaults.api_base_url = api_url

    creds, url = credentials.default()

    assert creds.key == api_key
    assert creds.secret == api_secret
    assert url == api_url


@patch.object(credentials, 'defaults')
def test_load_from_file(mock_defaults):

    api_key = utils.random_string()
    api_secret = utils.random_string()
    api_url = utils.random_string()

    content = {
        'current_profile': 'test',
        'profiles': {
            'test': {
                'api_url': api_url,
                'api_key': api_key,
                'api_secret': api_secret
            }
        }
    }

    for ext in ('yml', 'yaml', 'json'):
        with utils.tempdir() as tmpdir:
            filename = 'credentials.{}'.format(ext)
            serializer = json.dumps if ext == 'json' else yaml.dump

            with open(os.path.join(tmpdir, filename), 'w') as f:
                f.write(serializer(content))

            mock_defaults.credentials_path = tmpdir
            mock_defaults.credentials_filename = 'credentials'

            mock_defaults.api_key = api_key
            mock_defaults.api_secret = api_secret
            mock_defaults.api_base_url = api_url

            creds, url = credentials.default()

            assert url == api_url
            assert creds.key == api_key, ext
            assert creds.secret == api_secret


@patch.object(credentials, 'defaults')
def test_missing_required_values(mock_defaults):
    api_secret = utils.random_string()

    content = {
        'current_profile': 'test',
        'profiles': {
            'test': {
                'api_secret': api_secret
            }
        }
    }

    for ext in ('yml', 'yaml', 'json'):
        with utils.tempdir() as tmpdir:
            filename = 'credentials.{}'.format(ext)
            serializer = json.dumps if ext == 'json' else yaml.dump

            with open(os.path.join(tmpdir, filename), 'w') as f:
                f.write(serializer(content))

            mock_defaults.credentials_path = tmpdir
            mock_defaults.credentials_filename = 'credentials'
            mock_defaults.api_key = None
            mock_defaults.api_secret = None

            with pytest.raises(PureportError):
                credentials.default()


@patch.object(credentials, 'defaults')
def test_no_credentials(mock_defaults):
    with utils.tempdir() as tmpdir:
        mock_defaults.credentials_path = tmpdir
        mock_defaults.credentials_filename = 'credentials'
        mock_defaults.api_key = None
        mock_defaults.api_secret = None

        with pytest.raises(PureportError):
            credentials.default()
