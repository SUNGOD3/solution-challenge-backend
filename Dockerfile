FROM python:3.9.0-buster
MAINTAINER REXWU

ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app

WORKDIR $APP_DIR
COPY . $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r $APP_DIR/requirements/production.txt

WORKDIR $APP_DIR/src
CMD ["uwsgi", "--ini", "uwsgi.ini"]
