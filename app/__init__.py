from flask import Flask

from celery import Celery
from config import config, Config

from flask_caching import Cache

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
cache = None

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from .webui import webui
    from .api import api
    app.register_blueprint(webui)
    app.register_blueprint(api, url_prefix="/api")
    celery.conf.update(app.config)
    cache = Cache(app,app.config)
    return app