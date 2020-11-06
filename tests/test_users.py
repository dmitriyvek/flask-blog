import pytest

from flask_blog import db
from flask_blog.users.models import User
# from flask_blog.blog.models import Post
from flask_blog.users.services import generate_auth_token, decode_auth_token


def test_encode_and_decode_auth_token(app):
    with app.app_context():
        user = User.query.get(1)
        # db.session.delete(user)
        # db.session.commit()
        auth_token = generate_auth_token(user.id)

        assert isinstance(auth_token, bytes)
        assert decode_auth_token(auth_token) == user.id
