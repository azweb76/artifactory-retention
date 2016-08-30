from centos:7

MAINTAINER Dan Clayton <dclayton@godaddy.com>

WORKDIR /src

RUN yum install epel-release -y
RUN yum install python-pip git -y

COPY . /src/

RUN pip install /src/
