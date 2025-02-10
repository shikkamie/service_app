FROM python:3.12-alpine3.21

COPY requirements.txt /temp/reqiurements.txt
COPY service /service
WORKDIR /service
EXPOSE 8000

RUN pip install -r /temp/reqiurements.txt

RUN adduser --disabled-password service-user

USER service-user
