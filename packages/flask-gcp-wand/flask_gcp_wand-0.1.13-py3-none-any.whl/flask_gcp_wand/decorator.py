from http import HTTPStatus
from flask import Response
from .appengine.header import GaeHeader


def only_cloud_scheduler_for_gae_http(func):
    def wrapper(*args, **kwargs):
        if not GaeHeader.is_cloudscheduler_request():
            return Response(status=HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def only_cloud_tasks(func):
    def wrapper(*args, **kwargs):
        if not GaeHeader.is_tasks_request():
            return Response(status=HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
