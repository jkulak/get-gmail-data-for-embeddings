# jkulak/gmail-chat
FROM python:3.11.4-alpine3.18

RUN apk update && apk upgrade
RUN apk add --no-cache htop ncdu \
    && rm -rf /var/cache/apk/*

WORKDIR /app
ADD ./src/ ./
RUN pip install --no-cache-dir pipenv==v2023.7.23 && \
    pipenv install
