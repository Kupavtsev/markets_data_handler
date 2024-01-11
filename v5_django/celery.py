from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'v5_django.settings')

app = Celery('v5_django')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    
}

# Celery Beat Settings
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')