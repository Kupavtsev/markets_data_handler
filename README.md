Python 3.11.2

Django Quotes API Handler with Celery Workers (Redis)
Postgress data storage

# 1st bash
# Virtual env
pip install -r windows.txt
pip install -r linux.txt

mkdir "logs" in folder

# Redis
https://github.com/tporadowski/redis/releases

# 2nd bash
# Start Celery in paralel bash
celery -A v5_django.celery worker -l info
# for windows
celery -A v5_django.celery worker --pool=solo -l info

# 3rd bash
# Start Celery Beat
celery -A v5_django beat -l info

e.g.
--pool=solo
# prefork = we are using ChildProcessors
# concurrency = how much the Pools will be
# autoscale 10max 3min. How many ChildProcessors will work at the same time. 10 only if you have 10 CPU Cores.
--pool=prefork --concurrency=5 --autoscale=10,3