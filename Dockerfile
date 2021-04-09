FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install pipenv

COPY . /srv/app
WORKDIR /srv/app

COPY ./docker-entrypoint.sh /srv/app/docker-entrypoint.sh

COPY ./requirements.txt /srv/app/requirements.txt

COPY ./Pipfile /srv/app/Pipfile
COPY ./Pipfile.lock /srv/app/Pipfile.lock

RUN set -ex && pipenv install --deploy --system 

CMD ["bash", "/srv/app/docker-entrypoint.sh"]