FROM python:3.10-alpine
WORKDIR /code

COPY . /code


RUN pip install -r requirements.txt

