from .celery import app as celery_app

try:
    __all__ = ['celery_app']
except Exception as e:
    print('error', e)    