from flask import Blueprint

from flask_blog.users.api.views import UserRegisterAPI, UserLoginAPI, UserDetailAPI


users_blueprint = Blueprint('auth', __name__)


users_blueprint.add_url_rule(
    '/auth/register',
    view_func=UserRegisterAPI.as_view('register_api'),
    methods=['POST']
)

users_blueprint.add_url_rule(
    '/auth/login',
    view_func=UserLoginAPI.as_view('login_api'),
    methods=['POST']
)

users_blueprint.add_url_rule(
    '/auth/detail',
    view_func=UserDetailAPI.as_view('detail_api'),
    methods=['GET']
)
