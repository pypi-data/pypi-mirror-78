from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    EntryBlock


class ClassicNumbersItem(blocks.StructBlock):
    number = blocks.IntegerBlock(required=True)
    unit = blocks.CharBlock(required=False, help_text='unité de mesure')
    content = TextBlock(label="Content")


class NumbersEntry(EntryBlock):
    items = blocks.StreamBlock([
        ('classic', ClassicNumbersItem()),
    ], min_num=1)

    def mock(self, *args, **kwargs):
        classic = {
            'type': 'classic',
            'value': {
                'number': 90,
                'unit': '%',
                'content': {'value': self.p},
            }
        }

        self.mock_data.update({
            'type': 'numbers',
            'value': {
                'items': [classic, classic, classic, classic]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/numbers.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Numbers"
        icon = 'grip'
