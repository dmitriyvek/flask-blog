# Assuming that auth system has already been tested
import pytest
import json

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.blog.api.serializers import PostDetailSerializer


def test_post_detail_api_with_incorect_credentials(client):
    '''Test existed post detail view with not token provided and with invalid one'''
    post_id = 1

    with client:
        # without auth token
        response = client.get(f'/posts/{post_id}')
        assert response.status_code == 401

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Provide a valid auth credentials.'

        # with invalid auth token
        response = client.get(
            f'/posts/{post_id}',
            headers={
                'Authorization': 'Bearer incorrect_token',
            })
        assert response.status_code == 401

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Invalid token. Please log in again.'


def test_existed_post_detail_api(app, client, auth_token):
    '''Test existed post detail view with valid auth token'''
    post_id = 1
    with app.app_context():
        post = Post.query.get(post_id)

    with client:
        response = client.get(
            f'/posts/{post_id}',
            headers={
                'Authorization': f'Bearer {auth_token}',
            })
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'

        assert all(key in data['post'] for key in (
            'author_id', 'content', 'created_on', 'id', 'title', 'updated_on'))
        assert set(data['post'].values()) == set(
            PostDetailSerializer().dump(post).values())


def test_nonexisted_post_detail_api(app, client, auth_token):
    '''Test existed post detail view with valid auth token'''
    nonexisted_post_id = 100

    with client:
        response = client.get(
            f'/posts/{nonexisted_post_id}',
            headers={
                'Authorization': f'Bearer {auth_token}',
            })
        assert response.status_code == 404

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Item not found'
