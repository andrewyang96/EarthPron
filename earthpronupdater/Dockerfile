FROM ubuntu:latest

MAINTAINER Andrew Yang "ayang14@illinois.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y postgresql python-psycopg2 libpq-dev

COPY . /earthpronupdater
WORKDIR /earthpronupdater

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
