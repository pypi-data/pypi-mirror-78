from datetime import date
from django.db import models
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import fields
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from webspace.bakery.abstract import WagtailPageBakeryModel
from webspace.cms import constants
from webspace.cms.amp.mixins import AmpMixin
from webspace.cms.forms.abstract import FormMixin
from webspace.loader import get_model

from ._mixins import TagMixin

GenericPage = get_model('cms', 'GenericPage')


class APortfolioPageTag(TaggedItemBase):
    content_object = ParentalKey('PortfolioPage', related_name='tagged_items')

    class Meta:
        app_label = 'cms'
        abstract = True


class APortfolioPage(AmpMixin, FormMixin, WagtailPageBakeryModel, GenericPage):
    template = '%s/portfolio_page.html' % constants.PAGES_TEMPLATES_PATH
    cover = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    tags = ClusterTaggableManager(through='PortfolioPageTag', blank=True)
    date = models.DateTimeField("Date publication + tri", default=date.today)
    intro_title = models.CharField(
        default='',
        max_length=500,
        blank=True,
        help_text="Titre d'introduction qui s'affiche sur un block portfolio de présentation"
    )
    intro = models.CharField(
        default='',
        max_length=500,
        blank=True,
        help_text="Texte d'introduction qui s'affiche sur un block portfolio de présentation"
    )

    related_portfolio = StreamField([
        ('portfolio', blocks.PageChooserBlock(required=False, target_model='cms.PortfolioPage')),
    ], blank=True)

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]
    content_panels = [
                         StreamFieldPanel('cover'),
                         FieldPanel('date'),
                         FieldPanel('tags'),
                         FieldPanel('intro_title'),
                         FieldPanel('intro'),
                         StreamFieldPanel('related_portfolio'),
                     ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'

    def get_absolute_url(self):
        return self.full_url


class APortfolioIndexPage(TagMixin, AmpMixin, WagtailPageBakeryModel, GenericPage):
    subpage_types = ['PortfolioPage']
    template = '%s/portfolio_index_page.html' % constants.PAGES_TEMPLATES_PATH
    bg_desktop = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    bg_mobile = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    first_text = fields.RichTextField(default='', blank=True, features=settings.RICH_TEXT_FEATURES)

    content_panels = [
                         StreamFieldPanel('bg_desktop'),
                         StreamFieldPanel('bg_mobile'),
                         FieldPanel('first_text'),
                     ] + Page.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
