FROM python:3.8

RUN useradd -ms /bin/bash www
SHELL ["/bin/bash", "-c"]
USER www

RUN mkdir -p /home/www/code/myblog/log/{app,gunicorn}
RUN touch /home/www/code/myblog/log/app/{info.log,error.log}

WORKDIR /home/www/code/myblog

COPY requirements.txt requirements.txt
RUN python3 -m venv env
RUN env/bin/pip3 install -U pip
RUN env/bin/pip3 install -r requirements.txt

COPY config config
COPY flask_blog flask_blog
COPY migrations migrations
COPY bin bin 
COPY setup.py wsgi.py ./

# RUN chmod +x bin/start_gunicorn.sh
# RUN chown -R www:www /home/www/code
# USER www

EXPOSE 8001

ENTRYPOINT ["./bin/start_gunicorn.sh"]