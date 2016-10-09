FROM ubuntu:latest

MAINTAINER Andrew Yang "ayang14@illinois.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y sqlite3 libsqlite3-dev

COPY . /earthpron
WORKDIR /earthpron

RUN pip install -r requirements.txt

WORKDIR /earthpron/epapp
RUN sqlite3 earthpron.db < schema.sql

RUN printf '* * * * * * python update_db.py >> /tmp/update_log 2>&1\n\n' > /etc/crontab

ENTRYPOINT ["python"]
CMD ["app.py"]
