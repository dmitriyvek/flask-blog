from flask import Blueprint

from flask_blog.users.api.views import UserRegisterAPI, UserLoginAPI, UserDetailAPI, UserLogoutAPI, UserAccountConfirmationAPI


users_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


users_blueprint.add_url_rule(
    '/register',
    view_func=UserRegisterAPI.as_view('register_api'),
    methods=['POST']
)

users_blueprint.add_url_rule(
    '/login',
    view_func=UserLoginAPI.as_view('login_api'),
    methods=['POST']
)

users_blueprint.add_url_rule(
    '/detail',
    view_func=UserDetailAPI.as_view('detail_api'),
    methods=['GET']
)

users_blueprint.add_url_rule(
    '/logout',
    view_func=UserLogoutAPI.as_view('logout_api'),
    methods=['GET']
)

users_blueprint.add_url_rule(
    '/account_confirmation',
    view_func=UserAccountConfirmationAPI.as_view('account_confirmation_api'),
    methods=['GET']
)
