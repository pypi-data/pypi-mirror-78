from __future__ import absolute_import, unicode_literals

from django.core import management
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
app = Celery('webspace.cms')
app.config_from_object('webspace.cms.celeryconfig', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def bakery_build(self):
    logger.info(app.AsyncResult(self.request.id).state)
    management.call_command('build')
    print("bakery build")
