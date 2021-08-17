FROM python:3.7

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py migrate
RUN python manage.py collectstatic --no-input
