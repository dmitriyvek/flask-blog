# Assuming that auth system has already been tested
import pytest
import json

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.blog.api.serializers import PostDetailSerializer
from flask_blog.users.services import generate_auth_token


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
            }
        )
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
            '/posts',
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
            '/posts',
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
        '/posts',
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
        '/posts',
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
        '/posts',
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
        '/posts',
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


@pytest.mark.parametrize(('title', 'title_data', 'content', 'content_data'), (
    (True, 'new_unique_title', True, 'new_content'),
    (False, '', True, 'new_new_content'),
    (True, 'new_new_unique_title', True, ''),
    (True, 'new_new_unique_title', False, ''),
))
def test_existed_post_update_api(app, client, auth_token, title, title_data, content, content_data):
    '''Test existed post update view with valid auth token'''
    post_id = 1
    data = {
        'title': title_data,
        'content': content_data
    } if title and content else {
        'title': title_data
    } if title else {
        'content': content_data
    }

    with client:
        response = client.put(
            f'/posts/{post_id}',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'success'

        with app.app_context():
            post = Post.query.get(post_id)

        assert all(key in data['post']
                   for key in PostDetailSerializer().__dict__['fields'].keys())
        assert data['post'] == PostDetailSerializer().dump(post)


def test_post_update_with_not_author(app, client):
    '''Test update post by not author of this post'''
    post_id = 1
    with app.app_context():
        auth_token = generate_auth_token(user_id=2).decode('utf-8')

    with client:
        response = client.put(
            f'/posts/{post_id}',
            headers={
                'Authorization': f'Bearer {auth_token}',
            },
            data=json.dumps({
                'title': 'some'
            }),
            content_type='application/json'
        )
        assert response.status_code == 403
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'You are not allowed to change this resource.'


def test_post_delete_api(app, client, auth_token):
    '''Test post delete api with post\'s author'''
    post_id = 1

    with client:
        response = client.delete(
            f'/posts/{post_id}',
            headers={
                'Authorization': f'Bearer {auth_token}',
            }
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'Item successfully deleted.'

        with app.app_context():
            post = Post.query.get(post_id)
            assert post.is_deleted
