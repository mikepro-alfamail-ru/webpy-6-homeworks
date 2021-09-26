from celery import Celery


def make_celery(app=__name__):
    broker = 'redis://127.0.0.1:6379/2'
    backend = 'redis://127.0.0.1:6379/1'
    return Celery(app, backend=backend, broker=broker)


celery = make_celery()
