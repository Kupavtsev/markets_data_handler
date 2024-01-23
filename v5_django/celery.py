from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'v5_django.settings')

app = Celery('v5_django')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'get_data_binance_api' : {
        'task': 'get_data.tasks.check_response',
        'schedule': crontab(hour=16, minute=14),
        # 'args': (2,),   # you can pass this args to send_mail_func(args)
    }
}

# Celery Settings
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')