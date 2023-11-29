from celery import Celery
from django.conf import settings
import os


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'config.settings'
)


app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

