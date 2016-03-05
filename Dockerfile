FROM ubuntu:14.04

MAINTAINER Ivo Lima <ivo.romario@gmail.com>

ENV PYTHONUNBUFFERED 1

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python python-pip

RUN mkdir /code

WORKDIR /code

ADD . /code/
#ADD requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 8000
