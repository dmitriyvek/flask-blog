from flask import Blueprint

from flask_blog.blog.api.views import PostDetailUpdateDeleteAPI, PostListCreateAPI


posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


posts_blueprint.add_url_rule(
    '/<int:post_id>',
    view_func=PostDetailUpdateDeleteAPI.as_view('post_detail_viewset'),
    methods=['GET', 'PUT', 'DELETE']
)

posts_blueprint.add_url_rule(
    '',
    view_func=PostListCreateAPI.as_view('post_list_viewset'),
    methods=['GET', 'POST']
)
