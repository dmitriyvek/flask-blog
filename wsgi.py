import os

from dotenv import load_dotenv

from flask_blog import create_app
from flask_blog.blog import models as blog_models
from flask_blog.users import models as user_models


# load_dotenv()

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
