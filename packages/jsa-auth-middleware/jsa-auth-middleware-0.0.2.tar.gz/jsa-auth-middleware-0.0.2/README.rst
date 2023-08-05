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

2. Add `jsa_auth_middleware.JSAMiddleware` to your `MIDDLEWARE` configuration in `settings.py` to validate authentication of all incoming requests::

    MIDDLEWARE = [
        ...
        'jsa_auth_middleware.JSAMiddleware',
    ]

3. Import Query Response across application to define and process API response::

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

