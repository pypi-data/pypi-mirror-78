from django.db import models
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel
from wagtail.core.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock
from modelcluster.models import ClusterableModel
from webspace.loader import get_class


ButtonBlock = get_class('cms.blocks.common', 'ButtonBlock')
LinkBlock = get_class('cms.blocks.common', 'LinkBlock')
StreamCard = get_class('cms.blocks.entries', 'StreamCard')


class ANavigation(ClusterableModel):
    help_text = models.CharField(max_length=100, default='', blank=True)

    footer = StreamField([
        ('menu', SnippetChooserBlock('cms.Menu', required=False)),
        ('stream_card', StreamCard())
    ], blank=True, verbose_name="Footer items")

    header_menus = StreamField([
        ('menu', SnippetChooserBlock('cms.Menu', required=False)),
        ('link', LinkBlock())
    ], blank=True, verbose_name="Header items")

    header_buttons = StreamField([
        ('button', ButtonBlock())
    ], blank=True, verbose_name="Header button")

    panels = [
        FieldPanel("help_text"),
        StreamFieldPanel('header_menus'),
        StreamFieldPanel('header_buttons'),
        StreamFieldPanel('footer'),
    ]

    def __str__(self):
        return self.help_text

    class Meta:
        abstract = True
        app_label = 'cms'
