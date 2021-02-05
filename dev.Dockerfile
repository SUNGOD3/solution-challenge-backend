FROM python:3.9.0-buster
MAINTAINER REXWU

RUN apt-get update
RUN apt-get install vim

ENV PYTHONUNBUFFERED 1
ENV BASE_DIR /usr/local
ENV APP_DIR $BASE_DIR/app

WORKDIR $APP_DIR
COPY . $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r $APP_DIR/requirements/dev.txt

WORKDIR $APP_DIR/src/backend
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
