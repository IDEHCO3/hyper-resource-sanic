from secure import SecureHeaders
from functools import wraps
from sanic.response import json
secure_headers = SecureHeaders()
def setup_middlewares(app):
    @app.middleware('response')
    async def set_secure_headers(request, response):
        secure_headers.sanic(response)
def authentication():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            print("Entrei em authentication")
            is_authenticated = True

            if is_authenticated:
                # the user is authorized.
                # run the handler method and return the response
                print("Authenticated")
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authenticated'}, 401)

        return decorated_function

    return decorator
def permission():
    def decorator(fp):
        @wraps(fp)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            print("Entrei em permission")
            is_authorized = True

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await fp(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator
