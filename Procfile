release: python manage.py migrate --noinput
dtb_worker: python run_polling.py
worker: celery -A dtb worker -P prefork --loglevel=INFO 
beat: celery -A dtb beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
