import os
from datetime import timedelta


class Config:
    """Parent configuration class."""
    FLASK_ENV = 'production'
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret'
    TOKEN_EXPIRATION_TIME = timedelta(minutes=5)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    FLASK_ENV = "development"
    DEBUG = True
    TOKEN_EXPIRATION_TIME = timedelta(days=1)
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
