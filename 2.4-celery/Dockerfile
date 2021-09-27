FROM python:3.7
WORKDIR /celeryapp
COPY ./app /celeryapp/app
COPY ./requirements.txt /celeryapp

RUN pip install -r /celeryapp/requirements.txt

ENV PYTHONPATH "/"


