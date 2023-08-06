Using the API Bindings
======================

The Pureport REST API is documented using the OpenAPI specification version
3.0.  The Pureport Python implementation provides direct bindings for the
OpenAPI specification.  Using the API bindings provides native Python functions
that wrap around the REST implementation.

Making the bindings
-------------------

By default, the Pureport Python implementation will generate the function
bindings when the `pureport.api` module is first loaded.  The module will first
create a new :doc:`Session object <session>` using the default credentials.

With the new Session object, the API module will download the OpenAPI
specification from the Pureport API and dynamically compile it into a set of
functions and a set of models.

Once the module has been loaded, you can easily consume the Pureport API by
calling native Python functions that map to Pureport API endpoints.  It does
this by dynamically creating a function that is named based on the
`operationId` value in the specification file.

Assume for we want to retrieve a list of all accounts for our give API key.
The OpenAPI specification shows the following:

    .. code-block:: json

        {
            "/accounts": {
                "get": {
                    "operationId": "findAllAccounts",
                    "responses": {
                        "default": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/Account"
                                        },
                                        "type": "array"
                                    }
                                }
                            },
                            "description": "default response"
                        }
                    },
                    "summary": "List accounts",
                }
            }
        }

When the specification is loaded and the bindings are generated, the above can
be called directly by using a modified form of the `operationId`.  All
functions names are convered from camel case to snake case.

For instance, if you wanted to get a list of all accounts on the server, you
can using the API bindings as below.

    .. code-block:: python

        >>> from pureport import api
        >>> api.find_all_accounts()
        [<pureport.models.Account object at 0x7f6d3604ed00>]


The return value from the bound function `find_all_accounts()` will return an
instance of a Model object. The next section will discuss models.


Using models
------------

With the Python bindings, the request and response objects are passed using
models instead of native Python dictionary objects.  Each function that
requires input and/or returns output does so using the appropriate model.

Returning our our example above, the return object from `find_all_accounts()`
will convert the response JSON blob into a typed instance of
`pureport.models.Account`.

The model for the return object is based on the defined schema in the OpenAPI
specification (in this case `#/components/schemas/Account`).  Below is a look
at the schema definition from the OpenAPI specification.

    .. code-block:: json

        {
            "Account": {
                "description": "A Pureport Account",
                "properties": {
                    "demo": {
                        "description": "Whether this account is for demonstration purposes.",
                        "type": "boolean"
                    },
                    "description": {
                        "description": "The description.",
                        "maxLength": 256,
                        "minLength": 0,
                        "type": "string"
                    },
                    "hasChildren": {
                        "description": "Whether this account is a parent account for any other accounts.",
                        "readOnly": true,
                        "type": "boolean"
                    },
                    "href": {
                        "description": "The URI of the Pureport asset.",
                        "readOnly": true,
                        "type": "string"
                    },
                    "id": {
                        "description": "The id is a unique identifier representing the account.",
                        "example": "ac-9ntgDlC2sW6TISmceo-Xsg",
                        "maxLength": 64,
                        "minLength": 1,
                        "type": "string"
                    },
                    "name": {
                        "description": "The name.",
                        "maxLength": 64,
                        "minLength": 1,
                        "type": "string"
                    },
                    "parent": {
                        "$ref": "#/components/schemas/Link"
                    },
                    "pricingHidden": {
                        "description": "Whether pricing information is restricted on this account.",
                        "readOnly": true,
                        "type": "boolean"
                    },
                    "showChildAccountPricing": {
                        "description": "Whether to show pricing information to child accounts of this account.",
                        "type": "boolean"
                    },
                    "supportedConnectionGroups": {
                        "description": "A collection of asset links for which Supported Connection Groups this account has access to.",
                        "example": [
                            {
                                "href": "/supportedConnections/groups/default",
                                "id": "default"
                            },
                            {
                                "href": "/supportedConnections/groups/portConnections",
                                "id": "portConnections"
                            }
                        ],
                        "items": {
                            "$ref": "#/components/schemas/Link"
                        },
                        "type": "array",
                        "uniqueItems": true
                    },
                    "tags": {
                        "additionalProperties": {
                            "description": "Key-value pairs to associate with the Pureport asset.",
                            "type": "string"
                        },
                        "description": "Key-value pairs to associate with the Pureport asset.",
                        "type": "object"
                    },
                    "technicalContactEmails": {
                        "description": "Email addresses of technical contacts for this account.",
                        "example": [
                            "admin@email.com"
                        ],
                        "items": {
                            "description": "Email addresses of technical contacts for this account.",
                            "example": "[\"admin@email.com\"]",
                            "type": "string"
                        },
                        "maxItems": 10,
                        "minItems": 0,
                        "type": "array",
                        "uniqueItems": true
                    },
                    "verified": {
                        "description": "Whether this account has been verified by Pureport operations.",
                        "type": "boolean"
                    }
                },
                "required": [
                    "name"
                ],
                "type": "object"
            }
        }


All properties of of the returned object are based on the schema.  So for
instance if we wanted to get the value for `name` we can simply reference the
object property.

    .. code-block:: python

        >>> from pureport import api
        >>> accounts = api.find_all_accounts()
        >>> print(accounts[0].name)
        test account


    .. note::

        You can dump the entire model instance to a native Python dictionary by
        calling the `serialize()` method.


Models objects are also used as input to functions.  Let's assume we want to
create a new virtual network.  Based on the OpenAPI specification, we will need
to call `add_network()` and pass both an `account_id` and a `Network` object.

The relevant OpenAPI specification is below.

    .. code-block:: json

        {
            "/accounts/{accountId}/networks": {
                "post": {
                    "operationId": "addNetwork",
                    "parameters": [
                        {
                            "in": "path",
                            "name": "accountId",
                            "required": true,
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Network"
                                }
                            }
                        }
                    },
                    "responses": {
                        "default": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Network"
                                    }
                                }
                            },
                            "description": "default response"
                        }
                    },
                    "summary": "Add new network",
                }
            }
        }


Translating the OpenAPI specification into a set of Python calls would look
like the example below.

    .. code-block:: python

        >>> from pureport import defaults
        >>> from pureport import api
        >>> network = api.models.Network('demo network')
        >>> network
        <pureport.models.Network object at 0x7fc3933d0940>
        >>> api.add_network(defaults.account_id, network)
        <pureport.models.Network object at 0x7fc393cb04f0>



