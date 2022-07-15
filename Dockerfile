FROM python:3.8.6

COPY ./requirements.txt /django/

WORKDIR /django

RUN pip install --upgrade pip

RUN pip install -r requirements.txt