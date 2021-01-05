from flask import Flask
from flasgger import Swagger
from flask_debugtoolbar import DebugToolbarExtension
from flask_debug_api import DebugAPIExtension
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_migrate import Migrate

from config.settings import app_config
from config.swagger_conf import template
from flask_blog.db_engine import db
from flask_blog.loggers import get_main_logger


migrate = Migrate()
ma = Marshmallow()
mail = Mail()
swagger = Swagger(template=template)
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

    from flask_blog.cli_commands import init_db_data
    app.cli.add_command(init_db_data)

    if app.config['DEBUG']:
        DebugToolbarExtension(app)
        DebugAPIExtension(app)
        panels = list(app.config['DEBUG_TB_PANELS'])
        panels.append('flask_debug_api.BrowseAPIPanel')
        app.config['DEBUG_TB_PANELS'] = panels

    mail.init_app(app)
    app.extensions['mail'].debug = app.config['DEBUG']

    swagger.init_app(app)

    return app
