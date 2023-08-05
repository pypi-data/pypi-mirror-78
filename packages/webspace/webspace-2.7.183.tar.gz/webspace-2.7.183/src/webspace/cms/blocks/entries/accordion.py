from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    EntryBlock


class ClassicAccordionItem(blocks.StructBlock):
    head = TextBlock(label="Head")
    content = TextBlock(label="Head")


class AccordionEntry(EntryBlock):
    amp_scripts = ['accordion']
    items = blocks.StreamBlock([
        ('classic', ClassicAccordionItem()),
    ], min_num=1)

    def mock(self, *args, **kwargs):
        classic = {
            'type': 'classic',
            'value': {
                'head': {'value': self.p},
                'content': {'value': self.p},
            }
        }

        self.mock_data.update({
            'type': 'accordion',
            'value': {
                'items': [classic, classic, classic, classic]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/accordion.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Accordion"
        icon = 'list-ul'
