# -*- coding: utf-8 -*_
#
# Copyright (c) 2020, Pureport, Inc.
# All Rights Reserved

import os
import json

from ..utils import utils

from pureport import models


def make_schema():
    return {
        "TestSchema": {
            "properties": {
                "camelCase": {
                    "type": "string"
                },
                "snake_case": {
                    "type": "string"
                }
            }
        }
    }


def test_models_make():
    basepath = os.path.dirname(__file__)
    content = json.loads(open(os.path.join(basepath, '../openapi.json')).read())
    models.make(content)
    assert set(content['components']['schemas']).issubset(dir(models))


def test_models_dump():
    models.make({'components': {'schemas': make_schema()}})

    assert hasattr(models.TestSchema, 'camel_case')
    assert hasattr(models.TestSchema, 'snake_case')

    camel_case_value = utils.random_string()
    snake_case_value = utils.random_string()

    obj = models.TestSchema(
        camel_case=camel_case_value, snake_case=snake_case_value
    )

    resp = models.dump(obj)

    assert resp['camelCase'] == camel_case_value
    assert resp['snake_case'] == snake_case_value

    delattr(models, 'TestSchema')


def test_models_load():
    camel_case_value = utils.random_string()
    snake_case_value = utils.random_string()

    models.make({'components': {'schemas': make_schema()}})

    data = {'camel_case': camel_case_value, 'snake_case': snake_case_value}
    resp = models.load('TestSchema', data)

    assert isinstance(resp, models.TestSchema)
    assert resp.camel_case == camel_case_value
    assert resp.snake_case == snake_case_value

    delattr(models, 'TestSchema')
