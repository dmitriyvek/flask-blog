FROM python:3.8

RUN adduser www

RUN mkdir -p /home/www/code/myblog/log/{app,gunicorn}
WORKDIR /home/www/code/myblog

COPY requirements.txt requirements.txt
RUN python -m venv env
RUN env/bin/pip install -U pip
RUN env/bin/pip install -r requirements.txt

COPY config config
COPY flask_blog flask_blog
COPY migrations migrations
COPY bin bin 
COPY setup.py wsgi.py ./
RUN chmod +x bin/start_gunicorn.sh

ENV FLASK_APP wsgi.py

RUN chown -R www:www /home/www/code
USER www

EXPOSE 8001
ENTRYPOINT ["./bin/start_gunicorn.sh"]