from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class AGallery(index.Indexed, models.Model):
    help_text = models.CharField(max_length=100, default='', blank=True)

    medias = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)

    panels = [
        FieldPanel("help_text"),
        StreamFieldPanel('medias'),
    ]

    search_fields = [
        index.SearchField('help_text', partial_match=True),
    ]

    def __str__(self):
        return self.help_text

    class Meta:
        abstract = True
        app_label = 'cms'
