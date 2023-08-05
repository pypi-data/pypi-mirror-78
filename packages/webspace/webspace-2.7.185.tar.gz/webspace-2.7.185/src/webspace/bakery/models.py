from django.db import models
from django.conf import settings


class TaskBuild(models.Model):
    date_start = models.DateTimeField(null=True, blank=True, auto_now=True)
    date_end = models.DateTimeField(null=True, blank=True)
    task_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    ready = models.BooleanField(default=False)

    def __str__(self):
        return str(self.task_id)

    class Meta:
        ordering = ['-date_start']


class VersionBuild(models.Model):
    key = models.CharField(max_length=100, default=None, null=True, blank=True)
    total_build = models.IntegerField(default=0)

    def __str__(self):
        return "%s-%s" % (self.key, self.version)

    @staticmethod
    def get():
        bv, created = VersionBuild.objects.get_or_create(
            key='default',
        )
        if created:
            bv.save()
        return bv

    def minor(self):
        self.total_build += 1
        self.save()

    @property
    def version(self):
        return "%s-%s" % (settings.VERSION, str(self.total_build))
