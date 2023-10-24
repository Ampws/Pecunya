from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')

app = Celery('Pecunya')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(['CeleryTasks.tasks.listen_to_blockchain_task'])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)