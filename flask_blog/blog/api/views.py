from flask import request, make_response
from flask.views import MethodView
from flasgger import swag_from

from flask_blog.services import validate_input, validate_query_param
from flask_blog.wrappers import generic_error_logger
from flask_blog.blog.models import Post
from flask_blog.blog.services import (
    check_if_post_is_already_exist,
    check_if_user_is_post_author,
    create_and_return_new_post,
    get_post_list_chunk,
    mark_post_as_deleted,
    update_and_return_post,
)
from flask_blog.users.wrappers import login_required
from flask_blog.blog.api.serializers import (
    PostCreationSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostUpdateSerializer,
)


@generic_error_logger
class PostDetailUpdateDeleteAPI(MethodView):
    '''Post`s detail, update and delete resourse'''

    @swag_from('swagger/detail.yaml')
    def get(self, post_id):
        post = Post.query.get_object_or_404(id=post_id)
        response_object = {
            'status': 'success',
            'post': PostDetailSerializer().dump(post),
        }
        return make_response(response_object), 200

    @login_required
    @swag_from('swagger/update.yaml')
    def put(self, post_id):
        post = check_if_user_is_post_author(request.user_id, post_id)
        post_data = request.get_json()
        data = validate_input(post_data, PostUpdateSerializer)

        post = update_and_return_post(post, data)
        result = PostDetailSerializer().dump(post)
        response_object = {
            'status': 'success',
            'post': result,
        }
        return make_response(response_object), 200

    @login_required
    @swag_from('swagger/delete.yaml')
    def delete(self, post_id):
        post = check_if_user_is_post_author(request.user_id, post_id)
        mark_post_as_deleted(post)

        response_object = {
            'status': 'success',
            'message': 'Item successfully deleted.',
        }
        return make_response(response_object), 200


@generic_error_logger
class PostListCreateAPI(MethodView):
    '''Post list and creation resourse'''

    @swag_from('swagger/list.yaml')
    def get(self):
        query_params = [request.args.get(
            'last_message_index'), request.args.get('chunk_size')]
        last_message_index, chunk_size = validate_query_param(
            param=query_params, to_type=[int, int], many=True)

        post_list, new_last_message_index = get_post_list_chunk(
            last_message_index, chunk_size=chunk_size)
        result = PostListSerializer().dump(post_list, many=True)
        response_object = {
            'status': 'success',
            'post_list': result,
            'last_message_index': new_last_message_index
        }
        return make_response(response_object), 200

    @login_required
    @swag_from('swagger/create.yaml')
    def post(self):
        post_data = request.get_json()
        data = validate_input(post_data, PostCreationSerializer)
        check_if_post_is_already_exist(data['title'])

        post = create_and_return_new_post(data, request.user_id)
        result = PostDetailSerializer().dump(post)
        response_object = {
            'status': 'success',
            'post': result,
        }
        return make_response(response_object), 201
