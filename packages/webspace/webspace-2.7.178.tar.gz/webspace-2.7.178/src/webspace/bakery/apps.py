import fs
from django.apps import AppConfig
from webspace.bakery.signal_handlers import register_signal_handlers


class BakeryConfig(AppConfig):
    name = 'webspace.bakery'
    label = 'bakery'
    verbose_name = 'bakery'
    filesystem_name = "osfs:///"
    filesystem = fs.open_fs(filesystem_name)

    def ready(self):
        register_signal_handlers()
