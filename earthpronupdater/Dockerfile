FROM funkyfuture/deck-chores

RUN apk add --no-cache postgresql postgresql-dev
RUN apk add --no-cache gcc musl-dev

COPY . /earthpronupdater
WORKDIR /earthpronupdater

RUN pip install -r requirements.txt
