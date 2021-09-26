from flask import Flask
from app.celery_utils import init_celery


PKG_NAME = __name__


def create_app(app_name=PKG_NAME, **kwargs):
    app = Flask(app_name)
    if kwargs.get('celery'):
        init_celery(kwargs.get('celery'), app)
    from app.all import bp
    app.register_blueprint(bp)
    return app
