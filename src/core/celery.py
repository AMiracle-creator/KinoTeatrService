import os

from celery import Celery
from . import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('youtube')

app.config_from_object("django.conf:settings", namespace='CELERY')
app.conf.timezone = settings.TIME_ZONE

app.autodiscover_tasks(packages=['main'])
