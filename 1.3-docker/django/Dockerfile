FROM python:3.7

WORKDIR /dj_app

COPY ./dj_app /dj_app

RUN pip install -r /dj_app/requirements.txt
RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stocks_products.wsgi"]
