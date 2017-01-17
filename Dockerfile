FROM ubuntu:latest

MAINTAINER Andrew Yang "ayang14@illinois.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY . /earthpron
WORKDIR /earthpron

RUN pip install -r requirements.txt

WORKDIR /earthpron/EarthPronApp
RUN sqlite3 earthpron.db < schema.sql

ENTRYPOINT ["python"]
CMD ["app.py"]
