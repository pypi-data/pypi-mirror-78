Using Session Objects
=====================

The Pureport Python implementation provides a low level interface that handles
authenticating sessions, logging, and communciating with the Pureport REST API.

This section provides details regarding how to implement the Session object to
send and receive requests and responses.

Obtaining Credentials
---------------------

To get started building a new session, the library includes a convience
function for loading credentials.  Credentials can come from the environment or
credentials can be loaded from a configuration file.

The current order of precedence is to prefer credentials set as environment
variables and fall back to credentials provided via configuration files.

The Pureport API requires to separate values in order to authenticate a
request: an API key and an API secret.  API keys and secrets can be configured
in the `Pureport console <https://console.pureport.com>`_:

When loading from the environment, the credentials module looks for the
following environment variables:

    * PUREPORT_API_KEY
    * PUREPORT_API_SECRET

If the credentials module is unable to find the API keys provided in the
environment, then the credentials are loaded from a configuration file.  The
configuration file is loaded based on the following default locations:

    1) ~/.pureport/credentials.yml
    2) ~/.pureport/credentials.yaml
    3) ~/.pureport/credentials.json

The configuration file must be in the following structure:

    .. code-block:: yaml

        ---
        current_profile: development
        profiles:
            development:
                api_key: XXXXXXX
                api_secret: XXXXXX


To load the credentials, simply import the module and call the `default()`
function.

    .. code-block:: python

        from pureport import credentials
        keys, url = credentials.default()


The `default()` function will return a two value tuple.  The first element will
be a direction containing the discovered API key and API secret loaded as
disucssed above.  The second element will the base URL for communicating with
the Pureport API service.

    .. note::

        Typically you will not need to change the base URL value and the
        default will work with the production system.  This value is used for
        testing against non-production systems.

If the credentials are unable to locate a valid API key and API secret, the
credentials module will raise an error.

Once the credentials have been loaded, the next step is to create a Session
instance using the credentials.

The Session object
------------------

Session objects provide a base implementation for communciating with the
Pureport REST API.  Session objects provide native methods that map directly to
HTTP methods implemented on the transport.

The following creates a new Session objects with the default credentials:

    .. code-block:: python

        from pureport.credentials import default
        from pureport.session import Session

        session = Session(*default())
        response = session.get('/accounts')
        print(response.json)
        <output omitted>


The example above will create a new Session object, pass in the default
credentials and then call the `/accounts` URL using the HTTP GET method.  The
method will return a `pureport.transport.Response` instance.
