import datetime
from typing import Union

import jwt
from flask import abort, current_app, render_template, make_response, jsonify, url_for
from flask_mail import Message
from werkzeug.security import check_password_hash

from flask_blog import generic_logger, mail
from flask_blog.blog.models import Post
from flask_blog.users.models import BlacklistToken, User


logger = generic_logger


def generate_auth_token(user_id: int, email: str = '') -> bytes:
    '''Generates the Auth Token with the given user_id. If the email was also given then adds it to the payload (the token will be used account confirmation).'''
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + current_app.config.get('TOKEN_EXPIRATION_TIME'),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id,
        }
        if email:
            payload['email'] = email
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def check_if_token_is_blacklisted(token: str) -> None:
    '''Check if token is in the BlacklistToken table'''
    if BlacklistToken.query.filter_by(token=str(token)).first():
        error_message = {
            'status': 'fail',
            'message': 'Token is expired.'
        }
        abort(make_response(jsonify(error_message), 401))


def decode_token_and_return_payload(token: str, is_auth: bool = True) -> dict:
    '''Decodes given token and return payload or abort 401 error message if token is invalid.'''
    try:
        payload = jwt.decode(token, current_app.config.get(
            'SECRET_KEY'), algorithms=['HS256'])
        check_if_token_is_blacklisted(token)

        # if acoount confirmation token is used
        if (is_auth and payload.get('email')) or (not is_auth and not payload.get('email')):
            error_message = {
                'status': 'fail',
                'message': 'Invalid auth token is used.'
            }
            abort(make_response(jsonify(error_message), 401))

        return payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as error:
        error_message = {
            'status': 'fail',
            'message': 'Signature expired.' if error is jwt.ExpiredSignatureError else 'Invalid token.'
        }
        abort(make_response(jsonify(error_message), 401))


def create_blacklist_token(db, auth_token: str) -> None:
    '''Just creates blacklist token'''
    blacklist_token = BlacklistToken(token=auth_token)
    db.session.add(blacklist_token)
    db.session.commit()


def send_confirmation_email(data: dict, user_id: int) -> str:
    '''If registration email was given then send confirmation email with token. Returns corresponding message.'''
    if data.get('email'):
        try:
            confiramtion_token = generate_auth_token(
                user_id=user_id, email=data.get('email'))
            confirmation_url = url_for(
                'auth.account_confirmation_api', token=confiramtion_token, _external=True)
            message = Message(
                'Account confirmation',
                recipients=[data.get('email')],
                html=render_template('email/account_confirmation.html',
                                     username=data.get('username'), confirmation_url=confirmation_url)
            )
            mail.send(message)
            return 'An account confirmation message has been sent to your email.'

        except Exception as error:
            logger.error(error, exc_info=True)
            return 'There was an error in sending confirmation message on your email.'

    return 'Your new account is unconfirmed. You can set your email and request confirmation.'


def create_user(db, data: dict) -> dict:
    '''Creates new user. Returns generated auth token and message about account confirmation (send email message if email was given).'''
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password')
    )

    db.session.add(user)
    db.session.commit()

    return {
        'auth_token': generate_auth_token(user.id).decode('utf-8'),
        'message': send_confirmation_email(data, user_id=user.id)
    }


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
    if data.get('email'):
        user = User.query.filter((User.username == data.get('username')) | (
            User.email == data.get('email'))).first()
    else:
        user = User.query.filter_by(username=data.get('username')).first()

    if user:
        error_message = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        abort(make_response(jsonify(error_message), 202))


def get_user_with_post_list(user_id: int) -> User:
    '''Gets user with given id and all user\'s posts. Returns user with post_list in attributes'''
    user = User.query.get(user_id)
    user.posts = Post.query.\
        filter(Post.author_id == user_id, Post.is_deleted.is_(False)).\
        order_by(Post.created_on.desc()).\
        all()

    return user


def confirm_account_and_blacklist_token(db, data: dict, token: str) -> None:
    '''Confirm user account and black list token in one transaction. Aborts if email in token != email in table.'''
    user = User.query.get_object_or_404(id=data['sub'])
    if user.email != data['email']:
        error_message = {
            'status': 'fail',
            'message': 'Invalid confirmation token is used.'
        }
        abort(make_response(jsonify(error_message), 400))

    user.is_confirmed = True
    blacklist_token = BlacklistToken(token=token)
    db.session.add(blacklist_token)
    db.session.commit()
