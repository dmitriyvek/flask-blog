# source .env (before run test)

import pytest
from flask_migrate import upgrade

from flask_blog import create_app, db
from flask_blog.users.models import User
from flask_blog.blog.models import Post
from flask_blog.users.services import generate_auth_token


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        upgrade()

        user = User(
            username='test_user',
            password='test_pswd'
        )
        user2 = User(
            username='test_user_2',
            password='test_pswd'
        )

        post = Post(title='test_title', content='test_content', author=user)
        for i in range(6):
            post = Post(title=i, author=user)
        post.is_deleted = True

        db.session.add(user, user2)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()
        db.engine.execute('DROP TABLE alembic_version;')


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(app) -> str:
    with app.app_context():
        return generate_auth_token(user_id=1).decode('utf-8')
