import pytest
import json

from flask_blog import db
from flask_blog.blog.models import Post
from flask_blog.users.models import User
from flask_blog.users.services import generate_auth_token, decode_auth_token_and_return_sub
from flask_blog.users.api.serializers import UserDetailSerializer


def test_encode_and_decode_auth_token_and_return_sub(app):
    with app.app_context():
        user = User.query.get(1)
        auth_token = generate_auth_token(user.id)

        assert isinstance(auth_token, bytes)
        assert decode_auth_token_and_return_sub(auth_token) == user.id


def test_registration_with_new_user(client):
    with client:
        response = client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'registered_user',
                'password': 'test_pswd',
            }),
            content_type='application/json'
        )

        assert response.content_type == 'application/json'
        assert response.status_code == 201

        data = json.loads(response.data)
        assert all(key in data for key in ('status', 'auth_token'))
        assert data['status'] == 'success'
        assert data['auth_token']


def test_registered_with_already_registered_user(client):
    '''Test registration with not unique username'''

    with client:
        response = client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'test_user',
                'password': 'test_pswd',
            }),
            content_type='application/json'
        )

        assert response.status_code == 202
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert all(key in data for key in ('status', 'message'))
        assert data['status'] == 'fail'
        assert data['message'] == 'User already exists. Please Log in.'


def test_login_with_registered_user(client):
    with client:
        response = client.post(
            '/auth/login',
            data=json.dumps({
                'username': 'test_user',
                'password': 'test_pswd',
            }),
            content_type='application/json'
        )

        assert response.content_type == 'application/json'
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['auth_token']


def test_login_with_not_existed_user(client):
    '''Test for login of non-registered user'''
    with client:
        response = client.post(
            '/auth/login',
            data=json.dumps({
                'username': 'not_existed_user',
                'password': 'wrong_pswd',
            }),
            content_type='application/json'
        )
        assert response.content_type == 'application/json'
        assert response.status_code == 401

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'User with given credentials does not exist.'


def test_user_detail_api_after_login(app, client):
    '''Test access to user detail api with token given after loginig'''
    login_response = client.post(
        '/auth/login',
        data=json.dumps({
            'username': 'test_user',
            'password': 'test_pswd',
        }),
        content_type='application/json'
    )

    auth_token = json.loads(login_response.data)['auth_token']
    with client:
        response = client.get(
            '/auth/detail',
            headers={
                'Authorization': f'Bearer {auth_token}',
            }
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'success'

        with app.app_context():
            user = User.query.get(1)
            posts = Post.query.filter(Post.author_id == 1, Post.is_deleted.is_(
                False)).order_by(Post.created_on.desc()).all()
            user.posts = posts

        assert all(key in data['user']
                   for key in UserDetailSerializer().__dict__['fields'].keys())
        assert data['user'] == UserDetailSerializer().dump(user)


def test_user_detail_api_after_registration(client):
    '''Test access to user detail api with token given after registration'''
    register_response = client.post(
        '/auth/register',
        data=json.dumps({
            'username': 'new_user',
            'password': 'test_pswd',
        }),
        content_type='application/json'
    )

    auth_token = json.loads(register_response.data)['auth_token']
    with client:
        response = client.get(
            '/auth/detail',
            headers={
                'Authorization': f'Bearer {auth_token}',
            }
        )
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['user']['username'] == 'new_user'


def test_logout_with_valid_token(client, auth_token):
    '''Test logout with token before it expires'''
    with client:
        response = client.get(
            '/auth/logout',
            headers={
                'Authorization': f'Bearer {auth_token}',
            })
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'Successfully logged out.'

        # try to log out with blacklisted token
        response = client.get(
            '/auth/logout',
            headers={
                'Authorization': f'Bearer {auth_token}',
            })
        assert response.status_code == 401
        assert response.content_type == 'application/json'

        data = json.loads(response.data)
        assert data['status'] == 'fail'
        assert data['message'] == 'Token is blacklisted. Please log in again.'
