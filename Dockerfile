from python:3.7-slim-stretch

MAINTAINER Dan Clayton <dclayton@godaddy.com>

WORKDIR /src

COPY . /src/

RUN pip install /src/
