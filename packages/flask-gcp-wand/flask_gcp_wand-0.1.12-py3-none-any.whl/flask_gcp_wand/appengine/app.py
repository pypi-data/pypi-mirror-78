import logging
from flask import Flask
from .env import GaeEnv
from ..template.response import unexpected_error_response

DEFAULT_LOG_FORMAT = "%(funcName)s:%(lineno)d %(message)s"


def create_gae_flask_app(name, log_format=DEFAULT_LOG_FORMAT, **kwargs):
    setup_cloud_logging(log_format)
    app = Flask(name, **kwargs)
    setup_default_log_level(app)
    return app


def setup_cloud_logging(log_format=DEFAULT_LOG_FORMAT):
    logging.basicConfig(format="%(asctime)s %(levelname)s " + log_format)
    if GaeEnv.is_gae():
        from google.cloud.logging import Client
        from google.cloud.logging.handlers import setup_logging

        handler = Client().get_default_handler()
        formatter = logging.Formatter(fmt=log_format)
        handler.setFormatter(formatter)
        setup_logging(handler)


def setup_default_log_level(app):
    if GaeEnv.is_gae():
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)


def register_simple_error_handler(app):
    app.register_error_handler(Exception, unexpected_error_response)
