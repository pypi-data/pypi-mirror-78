from django.db import models
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from webspace.bakery.abstract import WagtailPageBakeryModel
from webspace.cms.amp.mixins import AmpMixin
from webspace.loader import get_model
from webspace.cms.forms.abstract import FormMixin

GenericPage = get_model('cms', 'GenericPage')
Form = get_model('cms', 'Form')


class AContactPage(AmpMixin, FormMixin, WagtailPageBakeryModel, GenericPage):
    form = models.ForeignKey(
        Form,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Formulaire",
    )

    content_panels = [
        SnippetChooserPanel('form')
    ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
