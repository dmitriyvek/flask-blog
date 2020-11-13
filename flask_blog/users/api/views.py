from flask import Response, request, make_response
from flask.views import MethodView

from flask_blog import db
from flask_blog.services import validate_input
from flask_blog.wrappers import generic_error_logger
from flask_blog.users.models import User
from flask_blog.users.services import create_blacklist_token, create_user_and_return_auth_token, check_credentials_and_get_auth_token, check_if_user_already_exist
from flask_blog.users.wrappers import login_required
from flask_blog.users.api.serializers import UserDetailSerializer, UserCreationSerializer


@generic_error_logger
class UserRegisterAPI(MethodView):
    '''User registration resource'''

    def post(self):
        post_data = request.get_json()
        data = validate_input(post_data, UserCreationSerializer)
        check_if_user_already_exist(data)

        auth_token = create_user_and_return_auth_token(
            db, data=data)
        response_object = {
            'status': 'success',
            'auth_token': auth_token
        }
        return make_response(response_object), 201


@generic_error_logger
class UserLoginAPI(MethodView):
    '''User login resourse'''

    def post(self):
        post_data = request.get_json()
        auth_token = check_credentials_and_get_auth_token(data=post_data)

        response_object = {
            'status': 'success',
            'auth_token': auth_token
        }
        return make_response(response_object), 200


@generic_error_logger
class UserDetailAPI(MethodView):
    '''User`s detail information resourse'''

    @login_required
    def get(self):
        user = User.query.get(request.user_id)
        response_object = {
            'status': 'success',
            'user': UserDetailSerializer().dump(user),
        }
        return make_response(response_object), 200


@generic_error_logger
class UserLogoutAPI(MethodView):
    '''Force token expire by adding it to the blacklist'''

    @login_required
    def get(self):
        auth_token = request.headers.get('Authorization').split(' ')[1]

        create_blacklist_token(db, auth_token)
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return make_response(response_object), 200
