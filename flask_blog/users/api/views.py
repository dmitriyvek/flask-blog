from flask import request, make_response, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash

from flask_blog import db
from flask_blog.users.models import User
from flask_blog.users.services import generate_auth_token, decode_auth_token_and_return_sub


class UserRegisterAPI(MethodView):
    '''User registration resource'''

    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(username=post_data.get('username')).first()

        if not user:
            try:
                user = User(
                    username=post_data.get('username'),
                    password=post_data.get('password')
                )

                db.session.add(user)
                db.session.commit()

                auth_token = generate_auth_token(user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode('utf-8')
                }
                return make_response(jsonify(response_object)), 201

            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response_object)), 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response_object)), 202


class UserLoginAPI(MethodView):
    '''User login resourse'''

    def post(self):
        post_data = request.get_json()
        try:
            user = User.query.filter_by(
                username=post_data.get('username')
            ).first()

            if user and check_password_hash(
                user.password, post_data.get('password')
            ):
                auth_token = generate_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response_object)), 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response_object)), 404

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


class UserDetailAPI(MethodView):
    '''User`s detail information resourse'''

    def get(self):
        auth_header = request.headers.get('Authorization')
        auth_token = ''

        if auth_header:
            auth_credentionals = auth_header.split(' ')
            if auth_credentionals[0] == 'Bearer':
                auth_token = auth_credentionals[1]

        if auth_token:
            sub_or_error_message = decode_auth_token_and_return_sub(auth_token)
            if not isinstance(sub_or_error_message, str):
                user = User.query.filter_by(id=sub_or_error_message).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'admin': user.admin,
                        'registered_on': user.registered_on
                    }
                }
                return make_response(jsonify(response_object)), 200

            response_object = {
                'status': 'fail',
                'message': sub_or_error_message
            }
            return make_response(jsonify(response_object)), 401

        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth credentionals.'
            }
            return make_response(jsonify(response_object)), 401
