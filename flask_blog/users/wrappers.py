from typing import Union
from types import FunctionType
from functools import wraps

from flask import Response, request, make_response

from flask_blog.users.services import decode_auth_token_and_return_sub


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
            sub_or_error_message = decode_auth_token_and_return_sub(auth_token)

            if isinstance(sub_or_error_message, int):
                request.user_id = sub_or_error_message
                return func(*args, **kwargs)

            error_message = sub_or_error_message
            response_object = {
                'status': 'fail',
                'message': error_message,
            }
            return make_response(response_object), 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth credentials.'
            }
            return make_response(response_object), 401

    return wrapped_func
