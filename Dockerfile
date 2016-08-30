from centos:7

MAINTAINER Dan Clayton <dclayton@godaddy.com>

WORKDIR /src

RUN yum install epel-release -y
RUN yum install python-pip git -y
RUN pip install git+https://www.github.com/azweb76/artifactory-retention
