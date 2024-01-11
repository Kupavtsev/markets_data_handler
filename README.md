Django Binance API Handler with Celery Workers (Redis)
Postgress data storage

# 1st bash
# Virtual env
pip install -r windows.txt
pip install -r linux.txt

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