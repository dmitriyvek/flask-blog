# My example flask blog

There is a link on [swagger](https://blog.dmitriyvek.com/apidocs)

## Project installation and setup

Getting project`s code

```
git clone https://github.com/dmitriyvek/flask-blog.git flask-blog
```

Install all requirements

```
cd flask-blog
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -e .
```

Create a .env file in project`s root with given parameters

```
FLASK_APP="wsgi.py"
SECRET_KEY="some_secret_string"
FLASK_ENV="(one of: development, production)"
APP_SETTINGS="(one of: development, production, testing, staging)"
DATABASE_URL="engine://user:pswd@host:port/table_name"
TEST_DATABASE_URL="engine://user:pswd@host:port/table_name"
INFO_LOG_FILE_LOCATION="unix-like location"
ERROR_LOG_FILE_LOCATION="unix-like location"

MAIL_SERVER=""
MAIL_PORT=INT
MAIL_USERNAME=""
MAIL_PASSWORD=""
MAIL_DEFAULT_SENDER=""
```

Change gunicorn configuration

```
vim config/gunicorn_config.py
vim bin/start_gunicorn.sh
```

Create a folder for gunicorn logs (where you specified it)

```
mkdir -p log/gunicorn
```

Starting gunicorn server

```
./bin/start_gunicorn.sh
```
