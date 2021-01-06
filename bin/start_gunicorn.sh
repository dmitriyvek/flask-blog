#!/bin/bash
source /home/www/code/myblog/env/bin/activate
source /home/www/code/myblog/.env
flask db upgrade
exec gunicorn -c "/home/www/code/myblog/config/gunicorn_config.py" wsgi:app