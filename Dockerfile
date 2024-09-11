FROM python:3.10.14-alpine3.20
LABEL authors="aleks"

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x docker/*.sh

#ENTRYPOINT ["sh", "/app/docker/start_app.sh"]
