import os

import pytest

from flask_blog import create_app


def test_development_config():
    app = create_app('development')
    assert app.config['FLASK_ENV'] == 'development'
    assert app.config['DEBUG']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URL')


def test_testing_config():
    app = create_app('testing')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv(
        'TEST_DATABASE_URL')
