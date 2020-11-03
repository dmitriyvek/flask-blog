import os

from dotenv import load_dotenv

from app import create_app
from app.blog import models as blog_models
from app.users import models as user_models


load_dotenv()

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)


if __name__ == '__main__':
    app.run()
