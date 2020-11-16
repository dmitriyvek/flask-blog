import os
from types import FunctionType
from typing import Union, List

from flask import abort, make_response, jsonify
from marshmallow import ValidationError

from flask_blog.loggers import INFO_LOG_FILE_LOCATION, ERROR_LOG_FILE_LOCATION


def init_logs() -> None:
    '''Creates log files inside log folder if it does not exist (unix only)'''
    if not os.path.exists(ERROR_LOG_FILE_LOCATION):
        os.mknod(ERROR_LOG_FILE_LOCATION)

    if not os.path.exists(INFO_LOG_FILE_LOCATION):
        os.mknod(INFO_LOG_FILE_LOCATION)


def validate_input(data: dict, serializer) -> dict:
    '''Validate given data with given Schema. If data is not valid abort 422 Response or 400 if no data provided.'''
    if not data:
        error_message = {
            'status': 'fail',
            'message': 'No data provided.'
        }
        abort(make_response(jsonify(error_message), 400))

    schema = serializer()
    try:
        validate_data = schema.load(data)
    except ValidationError:
        error_message = {
            'status': 'fail',
            'message': 'Invalid input.'
        }
        abort(make_response(jsonify(error_message), 422))

    return validate_data


def validate_query_param(param: Union[List[str], str], to_type: Union[List[FunctionType], FunctionType], many: bool = False) -> Union[List, Union[int, str]]:
    '''Casts and returns given query parameters to given types (int or str). If one of the parameters have invalid type aborts 400 Response'''
    if many and len(param) != len(to_type):
        raise ValueError(
            'Param list and to_type list should have same lenght.')

    try:
        if many:
            result = []
            for i in range(len(param)):
                if param[i]:
                    result.append(to_type[i](param[i]))
                else:
                    result.append(0 if to_type[i] is int else '')

        else:
            if param:
                result = to_type(param)
            else:
                result = 0 if to_type is int else ''

    except (ValueError, TypeError):
        error_message = {
            'status': 'fail',
            'message': 'Invalid query parameter type.'
        }
        abort(make_response(jsonify(error_message), 400))

    return result
