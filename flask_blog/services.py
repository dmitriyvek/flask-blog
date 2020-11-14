import os

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
