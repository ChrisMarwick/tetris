FROM python:3.13-alpine
COPY . usr/src
RUN chmod +x usr/src && cd usr/src && pip install poetry && poetry install --with webserver --without dev

CMD cd usr/src && poetry run gunicorn -b 0.0.0.0:8000 -k gevent -w 1 server:app
