from webspace.bakery.abstract import WagtailPageBakeryModel
from webspace.cms import constants
from webspace.cms.amp.mixins import AmpMixin
from webspace.loader import get_model
from webspace.cms.forms.abstract import FormMixin

GenericPage = get_model('cms', 'GenericPage')


class AHomePage(AmpMixin, FormMixin, WagtailPageBakeryModel, GenericPage):
    template = '%s/home_page.html' % constants.PAGES_TEMPLATES_PATH
    content_panels = GenericPage.content_panels

    subpage_types = [
        'cms.ContentPage',
        'cms.DocumentPage',
        'cms.BlogIndexPage',
        'cms.PortfolioIndexPage',
    ]

    class Meta:
        abstract = True
        app_label = 'cms'
