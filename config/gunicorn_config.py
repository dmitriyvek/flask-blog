# command = '/home/www/code/myblog/env/bin/gunicorn'
command = './env/bin/gunicorn'
# pythonpath = '/home/www/code/myblog'
pythonpath = '.'
bind = '0.0.0.0:8001'
workers = 3
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'FLASK_APP=wsgi.py'
loglevel = 'info'
# accesslog = '/home/www/code/myblog/log/gunicorn/access.log'
accesslog = '../log/gunicorn/access.log'
acceslogformat = '%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s'
errorlog = '../log/gunicorn/error.log'
