from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.common import \
    SvgBlock, \
    ImageBlock, \
    TextBlock, \
    EntryBlock


class SvgCell(SvgBlock):
    pass


class ImageCell(ImageBlock):
    pass


class TextCell(TextBlock):
    pass


class TableEntry(EntryBlock):
    rows = blocks.StreamBlock([
        ('cells', blocks.StreamBlock([
            ('text', TextCell()),
            ('svg', SvgCell()),
            ('image', ImageCell()),
        ], min_num=1)),
    ], min_num=1)

    def mock(self, *args, **kwargs):
        if 'theme' in kwargs:
            svg = self.SVG_ICON_LIGHT \
                if kwargs['theme'] == constants.THEME_LIGHT \
                else self.SVG_ICON_SPACE
        else:
            svg = self.SVG_ICON_SPACE
        if 'theme' in kwargs:
            image = self.IMG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT \
                else self.IMG_SQUARE_SPACE
        else:
            image = self.IMG_SQUARE_SPACE
        cell_text = {
            'type': 'text',
            'value': {
                'value': self.p,
            }
        }
        cell_svg = {
            'type': 'svg',
            'value': {
                'file': self.file(svg).id,
            }
        }
        cell_image = {
            'type': 'image',
            'value': {
                'file': self.file(image).id,
            }
        }

        self.mock_data.update({
            'type': 'table',
            'value': {
                'rows': [
                    {
                        'type': 'cells',
                        'value': [cell_text, cell_text, cell_text, cell_text]
                    },
                    {
                        'type': 'cells',
                        'value': [cell_text, cell_image, cell_text, cell_text]
                    },
                    {
                        'type': 'cells',
                        'value': [cell_text, cell_text, cell_text, cell_text]
                    },
                    {
                        'type': 'cells',
                        'value': [cell_text, cell_text, cell_text, cell_svg]
                    },
                ]
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/table.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Table"
        icon = 'grip'
