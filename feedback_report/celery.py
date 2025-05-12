
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feedback_report.settings")
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1') 
app = Celery("feedback_report")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
