import logging
from django.http import HttpResponse
from django.shortcuts import render

from webspace.cms import constants
from webspace.cms.celery import bakery_build, app

logger = logging.getLogger('bakery')


def index(request):
    return render(
        request,
        '%s/bakery.html' % constants.ADMIN_TEMPLATES_PATH,
        {'cache_icon': 'cog'}
    )


def build(request):
    last_id = request.session.get('last_bakery_task_id', None)
    if last_id:
        task = app.AsyncResult(last_id)
        if task.ready():
            task = bakery_build.delay()
            request.session['last_bakery_task_id'] = task.id
            return HttpResponse("Build is running !")
        return HttpResponse("Build is already running !")
    else:
        task = bakery_build.delay()
        request.session['last_bakery_task_id'] = task.id
        return HttpResponse("Build is running !")
