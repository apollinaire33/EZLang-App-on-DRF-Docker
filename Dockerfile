FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

COPY . /srv/app
WORKDIR /srv/app

COPY ./requirements.txt /srv/app/requirements.txt
RUN pip install -r /srv/app/requirements.txt