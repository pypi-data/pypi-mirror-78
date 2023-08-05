from wagtail.core import blocks

from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    ButtonsBlock, EntryBlock, FormBlock


class StreamContentEntry(EntryBlock):
    animation = blocks.BooleanBlock(required=False, help_text="Animation")
    align = AlignTextChoiceBlock(required=False)
    content = blocks.StreamBlock(
        [
            ('text', TextBlock()),
            ('buttons', ButtonsBlock()),
            ('form', FormBlock()),

        ],
        required=False
    )

    def mock(self, align='center', button_1=constants.BUTTON_PRIMARY,
             button_2=constants.BUTTON_PRIMARY_FULL, *args, **kwargs):
        self.mock_data.update({
            'type': 'stream_content',
            'value': {
                'content': [
                    {
                        'type': 'text',
                        'value': {
                            'value': self.text_first_content,
                        }
                    },
                    {
                        'type': 'buttons',
                        'value': [{
                            'type': 'button',
                            'value': self.button(button_1)
                        }, {
                            'type': 'button',
                            'value': self.button(button_2)
                        }],
                    },
                ],
                'align': align
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/stream_content.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Stream Content"
        icon = 'grip'
