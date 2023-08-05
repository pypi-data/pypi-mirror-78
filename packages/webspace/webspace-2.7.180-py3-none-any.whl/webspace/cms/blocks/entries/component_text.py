from wagtail.core import blocks

from webspace.cms.blocks.choice import AlignTextChoiceBlock
from webspace.cms import constants
from webspace.cms.blocks.common import \
    TextBlock, \
    SvgWithSizeBlock, \
    ImageWithSizeBlock, \
    ButtonBlock, \
    EntryBlock, \
    EmbedWithSizeBlock, \
    FormBlock, \
    GallerySliderBlock


class ComponentTextEntry(EntryBlock):
    amp_scripts = ['iframe', 'form']
    titles = TextBlock(label="Titres")
    text = TextBlock(label="Description")
    reverse = blocks.BooleanBlock(required=False, help_text="Permet de d'intervertir le component et la zone de texte")
    section = blocks.BooleanBlock(required=False, help_text="Permet de sectionner la zone de texte")
    animation = blocks.BooleanBlock(required=False, help_text="Animation")
    align = AlignTextChoiceBlock(required=False)
    component = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
            ('embed', EmbedWithSizeBlock()),
            ('form', FormBlock()),
            ('gallery_slider', GallerySliderBlock())
        ],
        max_num=1,
        required=False
    )
    buttons = blocks.StreamBlock(
        [
            ('button', ButtonBlock()),
        ],
        max_num=2, required=False
    )

    def mock(self, component='svg', align=None,
             section=False, reverse=False, size_component='m', button_1=constants.BUTTON_PRIMARY_FULL, button_2=None,
             *args, **kwargs):
        if component == 'svg':
            if 'theme' in kwargs:
                file = self.SVG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.SVG_SQUARE_SPACE
            else:
                file = self.SVG_SQUARE_SPACE
        else:
            if 'theme' in kwargs:
                file = self.IMG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT else self.IMG_SQUARE_SPACE
            else:
                file = self.IMG_SQUARE_SPACE
        ret = {
            'type': 'component_text',
            'value': {
                'titles': {'value': self.h1},
                'text': {
                    'value': self.normal
                },
                'component': [{
                    'type': component,
                    'value': {
                        'file': self.file(file).id,
                        'size': size_component
                    },
                }],
                'buttons': [],
                'reverse': reverse,
                'align': align,
                'section': section
            }
        }
        if component == 'embed':
            ret['value']['component'] = [{
                'type': 'embed',
                'value': {
                    'link': self.URL_EMBED,
                    'size': size_component
                }
            }]
        if component == 'form':
            form = self.get_form('small', 2, head_text=False)
            ret['value']['component'] = [{
                'type': 'form',
                'value': {
                    'form': form.id,
                }
            }]
        if button_1:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.button(button_1)
            })
        if button_2:
            ret['value']['buttons'].append({
                'type': 'button',
                'value': self.button(m_type=button_2)
            })
        self.mock_data.update(ret)
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/component_text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Component Text"
        icon = 'grip'
