from celery import Celery, shared_task
from celery.schedules import crontab
from deal_search.models import Notification

app = Celery()

@app.task
def notify_new_deals():
  Notification.fetch_items_and_notify_all()
