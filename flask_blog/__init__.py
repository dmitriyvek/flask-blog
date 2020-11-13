from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from config.settings import app_config
from flask_blog.db_engine import db
from flask_blog.loggers import get_main_logger


migrate = Migrate()
ma = Marshmallow()
generic_logger = get_main_logger()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from flask_blog.users.api.urls import users_blueprint
    from flask_blog.blog.api.urls import posts_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)

    return app
