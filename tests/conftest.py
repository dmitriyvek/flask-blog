import pytest
from flask_migrate import upgrade

from flask_blog import create_app, db
from flask_blog.users.models import User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        upgrade()

        user = User(
            username='test_user',
            password='test_pswd'
        )
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()
        db.engine.execute('DROP TABLE alembic_version;')


@pytest.fixture
def client(app):
    return app.test_client()
