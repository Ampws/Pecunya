import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

from celery import Celery

app = Celery('Home')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'redis://localhost:6379/0'
