from __future__ import absolute_import, unicode_literals
from datetime import datetime
from django.core import management
from celery import Celery
import os
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
app = Celery('webspace.bakery')
app.config_from_object('webspace.bakery.celeryconfig', namespace='CELERY')
app.conf.task_default_queue = settings.SITE_NAME
app.control.purge()
app.autodiscover_tasks()


@app.task(bind=True)
def bakery_build(self):
    from .models import TaskBuild
    task_obj = TaskBuild.objects.create()
    task_obj.task_id = self.request.id
    task_obj.save()
    management.call_command('build')
    task_obj.date_end = datetime.now()
    task_obj.ready = True
    task_obj.save()
