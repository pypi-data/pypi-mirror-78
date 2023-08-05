from django.urls import include, path, reverse
from wagtail.admin.menu import MenuItem
from wagtail.core import hooks

from webspace.bakery import urls as urls_bakery


class BakeryItem(MenuItem):
    """
    Registers wagtail-cache in wagtail admin for superusers.
    """

    def is_shown(self, request):
        return request.user.is_superuser


@hooks.register('register_admin_urls')
def register_admin_urls():
    """
    Registers wagtail-cache urls in the wagtail admin.
    """
    return [
        path('bakery/', include((urls_bakery, 'bakery'), namespace='bakery')),
    ]


@hooks.register('register_settings_menu_item')
def register_cache_menu():
    """
    Registers bakery settings panel in the wagtail admin.
    """
    return BakeryItem(
        'Bakery',
        reverse('bakery:index'),
        classnames='icon icon-cog')
