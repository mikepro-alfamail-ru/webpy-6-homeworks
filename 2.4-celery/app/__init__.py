from celery import Celery


def make_celery(app=__name__):
    broker = 'redis://redis:6379/2'
    backend = 'redis://redis:6379/1'
    return Celery(app, backend=backend, broker=broker)


celery = make_celery()
