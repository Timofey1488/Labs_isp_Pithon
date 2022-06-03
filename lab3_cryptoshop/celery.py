import os
from celery import Celery
#  setting for celery will install in our setting automatic
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab3_cryptoshop.settings')

app = Celery('lab3_cryptoshop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()  # search all files celery
