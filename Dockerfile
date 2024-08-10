FROM python:3.10.14-alpine3.20
LABEL authors="aleks"

RUN mkdir /app
WORKDIR /app

RUN apk update && apk upgrade && apk add bash

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
