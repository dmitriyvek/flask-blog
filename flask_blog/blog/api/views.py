from flask import Response, request, make_response
from flask.views import MethodView

from flask_blog import db
from flask_blog.users.wrappers import login_required
from flask_blog.blog.models import Post
from flask_blog.users.models import User
from flask_blog.blog.api.serializers import PostDetailSerializer, PostCreationSerializer
from flask_blog.blog.services import validate_input, create_and_return_new_post, check_if_post_is_already_exist


class PostDetailAPI(MethodView):
    '''Post`s detail information resourse'''

    def get(self, post_id):
        post = Post.query.get_object_or_404(id=post_id)
        response_object = {
            'status': 'success',
            'post': PostDetailSerializer().dump(post),
        }
        return make_response(response_object), 200


class PostCreateAPI(MethodView):
    '''New Post creation resourse'''

    @login_required
    def post(self):
        json_data = request.get_json()
        data = validate_input(json_data, PostCreationSerializer)
        check_if_post_is_already_exist(data)

        post = create_and_return_new_post(data, request.user_id)
        result = PostDetailSerializer().dump(post)
        response_object = {
            'status': 'success',
            'post': result,
        }
        return make_response(response_object), 201
