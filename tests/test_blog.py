# Assuming that auth system has already been tested
import pytest
import json

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.blog.api.serializers import PostDetailSerializer


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
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'success'

        assert all(key in data['post']
                   for key in PostDetailSerializer().__dict__['fields'].keys())
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
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Item not found'


def test_post_create_api_with_incorect_credentials(client):
    '''Test post create view with not token provided and with invalid one'''

    with client:
        # without auth token
        response = client.post(
            '/posts/create',
            data={
                'title': 'new_title',
                'content': 'new_content',
            }
        )
        assert response.status_code == 401
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Provide a valid auth credentials.'

        # with invalid auth token
        response = client.post(
            '/posts/create',
            headers={
                'Authorization': 'Bearer incorrect_token',
            },
            data=json.dumps({
                'title': 'new_title',
                'content': 'new_content',
            }),
            content_type='application/json'
        )
        assert response.status_code == 401
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Invalid token. Please log in again.'


def test_post_create_api(app, client, auth_token):
    '''Test post create view with correct credentials'''
    response = client.post(
        '/posts/create',
        headers={
            'Authorization': f'Bearer {auth_token}',
        },
        data=json.dumps({
            'title': 'new_title',
            'content': 'new_content',
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.content_type == 'application/json'

    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert all(key in data['post']
               for key in PostDetailSerializer().__dict__['fields'].keys())

    post_id = data['post']['id']
    with app.app_context():
        post = Post.query.get(post_id)

    assert set(data['post'].values()) == set(
        PostDetailSerializer().dump(post).values())


def test_post_create_api_with_existed_title(client, auth_token):
    '''Test post create view with correct credentials but with already existed title'''
    response = client.post(
        '/posts/create',
        headers={
            'Authorization': f'Bearer {auth_token}',
        },
        data=json.dumps({
            'title': 'test_title',
            'content': 'test_content',
        }),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert response.content_type == 'application/json'

    data = json.loads(response.data)
    assert data['status'] == 'fail'
    assert data['message'] == 'Post with given title is already exist.'


def test_post_create_api_with_empty_data(client, auth_token):
    '''Test post create view with correct credentials but with empty data'''
    response = client.post(
        '/posts/create',
        headers={
            'Authorization': f'Bearer {auth_token}',
        },
    )
    assert response.status_code == 400
    assert response.content_type == 'application/json'

    data = json.loads(response.data)
    assert data['status'] == 'fail'
    assert data['message'] == 'No data provided.'


def test_post_create_api_with_empty_title(client, auth_token):
    '''Test post create view with correct credentials but with empty title'''
    response = client.post(
        '/posts/create',
        headers={
            'Authorization': f'Bearer {auth_token}',
        },
        data=json.dumps({
            'title': '',
            'content': 'test_content',
        }),
        content_type='application/json'
    )
    assert response.status_code == 422
    assert response.content_type == 'application/json'

    data = json.loads(response.data)
    assert data['status'] == 'fail'
    assert data['message'] == 'Invalid input.'
