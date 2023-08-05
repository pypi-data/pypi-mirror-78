import logging
from django.http import HttpResponse
from django.shortcuts import render

from webspace.cms import constants

from .celery import bakery_build, app
from .models import TaskBuild

logger = logging.getLogger('bakery')


def index(request):
    task = TaskBuild.objects.first()
    return render(
        request,
        '%s/bakery.html' % constants.ADMIN_TEMPLATES_PATH,
        {
            'cache_icon': 'cog',
            'ready': task.ready if task else True,
            'builds': TaskBuild.objects.all()[:5]
         },
    )


def build(request):
    task = TaskBuild.objects.first()
    if not task or task.ready:
        bakery_build.delay()
        return HttpResponse("Build is running !")
    else:
        return HttpResponse("Build is already running !")
