from flask import Blueprint

from flask_blog.blog.api.views import PostDetailAndUpdateAPI, PostCreateAPI


posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


posts_blueprint.add_url_rule(
    '/<int:post_id>',
    view_func=PostDetailAndUpdateAPI.as_view('post_detail_api'),
    methods=['GET', 'PUT']
)

posts_blueprint.add_url_rule(
    '/create',
    view_func=PostCreateAPI.as_view('post_create_api'),
    methods=['POST']
)
