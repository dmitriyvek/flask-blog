from typing import Union
from types import FunctionType
from functools import wraps

from flask import Response, request, make_response

from flask_blog.users.services import decode_token_and_return_payload


def login_required(func: FunctionType) -> FunctionType:
    '''Decorator that checks request\'s authorization header: if it is ok then adds user_id to the request, if it is not then returns 404 response'''

    @wraps(func)
    def wrapped_func(*args, **kwargs) -> Union[Response, FunctionType]:
        auth_header = request.headers.get('Authorization')
        auth_token = ''

        if auth_header:
            auth_credentials = auth_header.split(' ')
            if auth_credentials[0] == 'Bearer':
                auth_token = auth_credentials[1]

        if auth_token:
            payload = decode_token_and_return_payload(auth_token)
            request.user_id = payload['sub']
            return func(*args, **kwargs)

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth credentials.'
            }
            return make_response(response_object), 401

    return wrapped_func
