from flask import Response, request, make_response, jsonify
from flask.views import MethodView

from flask_blog import db
from flask_blog.users.models import User, BlacklistToken
from flask_blog.users.api.serializers import UserDetailSerializer
from flask_blog.users.services import generate_auth_token, decode_auth_token_and_return_sub, create_blacklist_token, create_user_and_return_auth_token, check_credentials_and_get_auth_token
from flask_blog.users.wrappers import login_required


class UserRegisterAPI(MethodView):
    '''User registration resource'''

    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(username=post_data.get('username')).first()

        if not user:
            try:
                auth_token = create_user_and_return_auth_token(
                    db, data=post_data)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
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
            auth_token = check_credentials_and_get_auth_token(data=post_data)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return make_response(jsonify(response_object)), 200

            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User with given credentials does not exist.'
                }
                return make_response(jsonify(response_object)), 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object)), 500


class UserDetailAPI(MethodView):
    '''User`s detail information resourse'''

    @login_required
    def get(self):
        user = User.query.get(request.user_id)
        response_object = {
            'status': 'success',
            'user': UserDetailSerializer().dump(user),
        }
        return make_response(jsonify(response_object)), 200


class UserLogoutAPI(MethodView):
    '''Force token expire by adding it to the blacklist'''

    @login_required
    def get(self):
        auth_token = request.headers.get('Authorization').split(' ')[1]

        try:
            create_blacklist_token(db, auth_token)
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return make_response(jsonify(responseObject)), 200

        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': e
            }
            return make_response(jsonify(responseObject)), 200
