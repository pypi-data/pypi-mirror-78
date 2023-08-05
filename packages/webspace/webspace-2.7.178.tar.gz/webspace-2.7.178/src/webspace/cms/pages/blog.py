from datetime import date
import re
import readtime
from lxml import etree

from django.shortcuts import render
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
from webspace.loader import get_model, get_class

from ._mixins import TagMixin

GenericPage = get_model('cms', 'GenericPage')
Person = get_model('cms', 'Person')

TextEntry = get_class('cms.blocks.entries', 'TextEntry')


class ABlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')

    class Meta:
        app_label = 'cms'
        abstract = True


class ABlogPage(AmpMixin, FormMixin, WagtailPageBakeryModel, GenericPage):
    template = '%s/blog_page.html' % constants.PAGES_TEMPLATES_PATH
    author = models.ForeignKey(
        Person,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    cover = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    bg_desktop = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    bg_mobile = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    tags = ClusterTaggableManager(through='BlogPageTag', blank=True)
    date = models.DateTimeField("Date publication + tri", default=date.today)
    date_updated = models.DateTimeField("Date mise à jour", default=None, null=True, blank=True)
    intro = models.CharField(
        default='',
        max_length=500,
        blank=True,
        help_text="Texte d'introduction qui s'affiche sur un block article de présentation"
    )
    intro_page = fields.RichTextField(
        default='',
        blank=True,
        features=settings.RICH_TEXT_FEATURES,
        help_text="Texte qui s'affiche sur un la page de l'article"
    )
    h1 = models.CharField('Titre intro', default='', max_length=200, blank=True)
    related_blogs = StreamField([
        ('article', blocks.PageChooserBlock(required=False, target_model='cms.BlogPage')),
    ], blank=True)

    promote_panels = GenericPage.promote_panels + [
        StreamFieldPanel('schemas'),
    ]
    content_panels = [
                         StreamFieldPanel('bg_desktop'),
                         StreamFieldPanel('bg_mobile'),
                         StreamFieldPanel('cover'),
                         FieldPanel('author'),
                         FieldPanel('date'),
                         FieldPanel('date_updated'),
                         FieldPanel('tags'),
                         FieldPanel('h1'),
                         FieldPanel('intro'),
                         FieldPanel('intro_page'),
                         StreamFieldPanel('related_blogs'),
                     ] + GenericPage.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'

    @property
    def blog_index(self):
        return self.get_ancestors().type(ABlogIndexPage).last()

    @property
    def read_time(self):
        rgx = re.compile(r'<.*?>')
        words = ""
        for block in self.body:
            if isinstance(block.block, TextEntry):
                text = block.value['text']['value'].source
                words += " " + rgx.sub('', text)
        return readtime.of_text(words)

    def get_absolute_url(self):
        return self.full_url

    def get_context(self, request, *args, **kwargs):
        context = super(ABlogPage, self).get_context(request)
        try:
            html = render(
                request,
                self.get_template(request, *args, **kwargs),
                context
            )
            tree = etree.HTML(html.content)
            summary = []
            for node in tree.xpath('//h2|//h3|//h4|//h5'):
                if node.attrib.get('id'):
                    if node.tag == 'h2':
                        summary.append({
                            'content': node.text,
                            'link': node.attrib.get('id'),
                            'h3': []
                        })
                    if node.tag == 'h3':
                        summary[-1]['h3'].append({
                            'content': node.text,
                            'link': node.attrib.get('id'),
                            'h4': []
                        })
                    """
                    if node.tag == 'h4':
                        summary[-1]['h3'][-1]['h4'].append({
                            'content': node.text,
                            'link': node.attrib.get('id'),
                        })
                    """
            context['summary'] = summary
        except Exception:
            context['summary'] = None
        return context


class ABlogIndexPage(TagMixin, AmpMixin, FormMixin, WagtailPageBakeryModel, GenericPage):
    subpage_types = ['BlogPage']
    template = '%s/blog_index_page.html' % constants.PAGES_TEMPLATES_PATH
    bg_desktop = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    bg_mobile = StreamField([
        ('image', ImageChooserBlock()),
        ('svg', DocumentChooserBlock()),
    ], blank=True)
    h1 = models.CharField(default='', max_length=200, blank=True)
    first_text = fields.RichTextField(default='', blank=True, features=settings.RICH_TEXT_FEATURES)

    content_panels = [
                         StreamFieldPanel('bg_desktop'),
                         StreamFieldPanel('bg_mobile'),
                         FieldPanel('h1'),
                         FieldPanel('first_text'),
                     ] + Page.content_panels

    class Meta:
        abstract = True
        app_label = 'cms'
