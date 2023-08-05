from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import EntryBlock


class PortfoliosEntry(EntryBlock):
    portfolios = blocks.StreamBlock(
        [
            ('portfolio', blocks.PageChooserBlock(required=False, target_model='cms.PortfolioPage')),
        ],
        min_num=1
    )

    class Meta:
        template = '%s/entries/portfolios.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Portfolios"
        icon = 'grip'
