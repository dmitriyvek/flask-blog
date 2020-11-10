from flask import Blueprint

from flask_blog.blog.api.views import PostDetailAPI


posts_blueprint = Blueprint('posts', __name__, url_prefix='/posts')


posts_blueprint.add_url_rule(
    '/<int:post_id>',
    view_func=PostDetailAPI.as_view('post_detail_api'),
    methods=['GET']
)
