from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.choice import ThemeChoiceBlock
from webspace.cms.blocks.common import \
    FormBlock, \
    EntryBlock


class FormEntry(EntryBlock):
    amp_scripts = ['form']
    theme_reverse = ThemeChoiceBlock(required=False)
    theme_content = ThemeChoiceBlock(required=False)

    form = FormBlock()

    def mock(self, *args, **kwargs):
        form = self.get_form('big')
        self.mock_data.update({
            'type': 'form',
            'value': {
                'form': {
                    'form': form.id
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/form.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Form"
        icon = 'form'
