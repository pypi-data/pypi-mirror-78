from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    EntryBlock, \
    ButtonBlock


class TimelineCustomBlock(TextBlock):
    icon = SnippetChooserBlock('cms.IconSnippet', required=True)
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=3,
        required=False
    )

    class Meta:
        template = '%s/common/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Custom"


class TimeLineEntry(EntryBlock):
    animation = blocks.BooleanBlock(required=False, help_text="Animation")
    items = blocks.StreamBlock(
        [
            ('text', TextBlock()),
            ('custom', TimelineCustomBlock()),
        ],
        min_num=1
    )

    def mock(self, *args, **kwargs):
        item = {
            'type': 'text',
            'value': {
                'value': self.xs
            }
        }
        self.mock_data.update({
            'type': 'timeline',
            'value': {
                'items': [
                    item,
                    item,
                    item,
                    item,
                    item
                ]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/timeline.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Timeline"
        icon = 'grip'
