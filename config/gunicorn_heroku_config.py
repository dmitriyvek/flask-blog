# gunicorn config for deployment on heroku

def when_ready(server):
    # touch app-initialized when ready
    open('/tmp/app-initialized', 'w').close()


bind = 'unix:///tmp/nginx.socket'
workers = 3
