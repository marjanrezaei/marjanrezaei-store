import os
from celery import Celery

# Set Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")  # Update with your actual project name

app = Celery("core")  # Project name
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

