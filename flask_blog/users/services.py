import datetime
from typing import Union

import jwt
from flask import current_app


def generate_auth_token(user_id) -> str:
    '''Generates the Auth Token with the given user_id'''
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + current_app.config.get('TOKEN_EXPIRATION_TIME'),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token) -> Union[int, str]:
    '''Decodes given auth_token and return user_id'''
    try:
        payload = jwt.decode(auth_token, current_app.config.get(
            'SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
