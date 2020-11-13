from functools import wraps

from flask import make_response
from werkzeug.exceptions import HTTPException

from flask_blog import generic_logger


def generic_error_handling_wrapper(logger):
    '''Wrapper for handling all not caught exceptions and log it in given logger'''

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)

            except HTTPException as error:
                return error.get_response()

            except Exception as error:
                logger.error(error, exc_info=True)
                response_object = {
                    'status': 'fail',
                }
                return make_response(response_object), 500

        return wrapper

    return decorator


def wrapp_all_methods(decorator):
    '''Wrap all class methods with given decorator'''

    def cls_wrapper(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return cls_wrapper


generic_error_logger = wrapp_all_methods(
    generic_error_handling_wrapper(generic_logger))
