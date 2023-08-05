from wagtail.core.fields import StreamField

from .email import EmailAction


class ActionManager(object):

    def __init__(self):
        pass

    def get_actions(self):
        return StreamField([
            ('email', EmailAction()),
        ], blank=True)
