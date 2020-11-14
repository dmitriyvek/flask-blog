import datetime
from typing import Union

import jwt
from flask import abort, current_app, make_response, jsonify
from werkzeug.security import check_password_hash

from flask_blog.users.models import BlacklistToken, User


def generate_auth_token(user_id: int) -> bytes:
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


def check_if_token_is_blacklisted(auth_token: str) -> bool:
    '''Check if auth_token is in the BlacklistToken table'''
    if BlacklistToken.query.filter_by(token=str(auth_token)).first():
        return True
    return False


def decode_auth_token_and_return_sub(auth_token: str) -> Union[int, str]:
    '''Decodes given auth_token and return user_id or error message if token is invalid'''
    try:
        payload = jwt.decode(auth_token, current_app.config.get(
            'SECRET_KEY'), algorithms=['HS256'])
        token_is_blacklisted = check_if_token_is_blacklisted(auth_token)

        if token_is_blacklisted:
            return 'Token is blacklisted. Please log in again.'

        return payload['sub']

    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def create_blacklist_token(db, auth_token: str) -> None:
    '''Just creates blacklist token'''
    blacklist_token = BlacklistToken(token=auth_token)
    db.session.add(blacklist_token)
    db.session.commit()


def create_user_and_return_auth_token(db, data: dict) -> str:
    '''Creates new user and return generated auth token for him'''
    user = User(
        username=data.get('username'),
        password=data.get('password')
    )

    db.session.add(user)
    db.session.commit()

    return generate_auth_token(user.id).decode('utf-8')


def check_credentials_and_get_auth_token(data: dict) -> str:
    '''Check if user with given credentials exist; if it does then returns auth token for him; if it does not then abort 401 Response'''
    user = User.query.filter_by(
        username=data.get('username')
    ).first()

    if not (user and check_password_hash(
        user.password, data.get('password')
    )):
        error_message = {
            'status': 'fail',
            'message': 'User with given credentials does not exist.'
        }
        abort(make_response(jsonify(error_message), 401))

    return generate_auth_token(user.id).decode('utf-8')


def check_if_user_already_exist(data: dict) -> None:
    '''Check if user with the given username is already exists. Aborts 202 Response if it does.'''
    user = User.query.filter_by(username=data.get('username')).first()

    if user:
        error_message = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        abort(make_response(jsonify(error_message), 202))
