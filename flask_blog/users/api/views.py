from flask import request, make_response
from flask.views import MethodView
from flasgger import swag_from

from flask_blog import db
from flask_blog.services import validate_input
from flask_blog.wrappers import generic_error_logger
from flask_blog.users.services import (
    check_credentials_and_get_auth_token,
    check_if_user_already_exist,
    confirm_account_and_blacklist_token,
    create_blacklist_token,
    create_user,
    decode_token_and_return_payload,
    get_user_with_post_list,
)
from flask_blog.users.wrappers import login_required
from flask_blog.users.api.serializers import (
    UserCreationSerializer,
    UserDetailSerializer,
)


@generic_error_logger
class UserRegisterAPI(MethodView):
    '''User registration resource'''

    @swag_from('swagger/registration.yaml')
    def post(self):
        post_data = request.get_json()
        data = validate_input(post_data, UserCreationSerializer)
        check_if_user_already_exist(data)

        user_data = create_user(
            db, data=data)
        response_object = {
            'status': 'success',
            **user_data
        }
        return make_response(response_object), 201


@generic_error_logger
class UserLoginAPI(MethodView):
    '''User login resourse'''

    @swag_from('swagger/login.yaml')
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
    @swag_from('swagger/detail.yaml')
    def get(self):
        user = get_user_with_post_list(request.user_id)
        response_object = {
            'status': 'success',
            'user': UserDetailSerializer().dump(user),
        }
        return make_response(response_object), 200


@generic_error_logger
class UserLogoutAPI(MethodView):
    '''Force token expire by adding it to the blacklist'''

    @login_required
    @swag_from('swagger/logout.yaml')
    def get(self):
        auth_token = request.headers.get('Authorization').split(' ')[1]

        create_blacklist_token(db, auth_token)
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return make_response(response_object), 200


@generic_error_logger
class UserAccountConfirmationAPI(MethodView):
    '''
    User account confirmation resourse (need token in query params)
    '''

    @swag_from('swagger/confirmation.yaml')
    def get(self):
        token = request.args.get('token')
        if not token:
            error_message = {
                'status': 'fail',
                'message': 'No confirmation token has been specified.'
            }
            return make_response(error_message), 400

        payload = decode_token_and_return_payload(token, is_auth=False)

        confirm_account_and_blacklist_token(db, payload, token)
        response_object = {
            'status': 'success',
            'message': 'Successfully confirmed your account.'
        }
        return make_response(response_object), 200
