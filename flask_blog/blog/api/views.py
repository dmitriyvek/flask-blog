from flask import Response, request, make_response, jsonify
from flask.views import MethodView

from flask_blog import db
from flask_blog.users.wrappers import login_required
from flask_blog.blog.models import Post
from flask_blog.blog.api.serializers import PostDetailSerializer


class PostDetailAPI(MethodView):
    '''Post`s detail information resourse'''

    @login_required
    def get(self, post_id):
        post = Post.query.get_object_or_404(id=post_id)
        response_object = {
            'status': 'success',
            'post': PostDetailSerializer().dump(post),
        }
        return make_response(jsonify(response_object)), 200
