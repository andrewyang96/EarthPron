FROM ubuntu:latest

MAINTAINER Andrew Yang "ayang14@illinois.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y postgresql python-psycopg2 libpq-dev
RUN apt-get install -y cron

COPY . /earthpronupdater
WORKDIR /earthpronupdater

RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
