FROM python:3.7.4-alpine3.10

WORKDIR /src

COPY . /src/

RUN pip install /src/

ENTRYPOINT ["artret"]
