====================================
JetStream Authentication Middleware
====================================

JSA Auth Middleware is a python package built
for integrating with JetStream across multiple
micro-services, with the aim of handling
authentication and Single-Sign-On while ensuring API security.


Quick start
-----------
1. Configure `AUTH_BASE_URL` in project `settings` pointing to the Authentication server **without trailing slash** 

2. Add `jsa_auth_middleware.JSAMiddleware` to your `MIDDLEWARE` configuration in `settings.py` to validate authentication of all incoming requests. Maintain the order and hierarchy of middlewares, with Django middlewares above JSAMiddleware. ::

    MIDDLEWARE = [
        ...
        'jsa_auth_middleware.JSAMiddleware',
    ]

3. Setup JSAMiddleware configuration in `settings.py`::

    JSA_AUTH_MIDDLEWARE_CONFIG = {
        'IGNORE_URLS': (
            '<<URL_TO_IGNORE>>',
        ),
        'IGNORE_STARTSWITH_URLS': (
            '<<URL_TO_IGNORE>>',
        ),
        'AUTH_BASE_URL': '', # optional if variable isn't in `settings.py`
    }

4. Import Query Response across application to define and process API response::

    from jsa_auth_middleware.query_response import Response


    resp = Response()
    resp.failed() # on failure, using default failure status_code
    resp.message = '<<Some response message>>'
    resp.add_params('<<data_key>>', <<data_value>>)


    resp = Response()
    resp.passed() # on success, using default success status_code
    resp.message = '<<Some response message>>'
    resp.add_params('<<data_key>>', <<data_value>>)


    # Setting response status code
    resp.status_code = <<CustomStatusCode>>


**NOTE**

The `IGNORE_STARTSWITH_URLS` in `JSA_AUTH_MIDDLEWARE_CONFIG` has the following default pre-defined endpoints patterns to be ignored::

    (
        "/admin/",
        "/swagger/",
        "/redoc/",
    )

