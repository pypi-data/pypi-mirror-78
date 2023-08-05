from wagtail.core import blocks

from webspace.cms import constants
from webspace.cms.blocks.choice import ThemeChoiceBlock
from webspace.cms.blocks.common import \
    SvgWithSizeBlock, \
    TextBlock, \
    ButtonBlock, \
    EntryBlock, \
    ImageWithSizeBlock, \
    PersonBlock, \
    IconTextBlock


class StreamCard(blocks.StructBlock):
    streams = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
            ('text', TextBlock()),
            ('icon_text', IconTextBlock())
        ],
        required=False
    )

    class Meta:
        template = '%s/common/cards/stream_card.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Stream Card"


# FIXME: remove CustomCard and merge it with StreamCard

class CustomCard(blocks.StructBlock):
    text = TextBlock()
    button = ButtonBlock()
    icon = SvgWithSizeBlock(label="Icon")
    media = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
        ],
        max_num=1,
        required=False
    )

    class Meta:
        template = '%s/common/cards/custom_card.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Custom Card"


class PersonCard(PersonBlock):
    pass


class ReviewCard(blocks.StructBlock):
    score = blocks.IntegerBlock()
    text = TextBlock()
    media = blocks.StreamBlock(
        [
            ('svg', SvgWithSizeBlock()),
            ('image', ImageWithSizeBlock()),
        ],
        max_num=1,
        required=False
    )

    class Meta:
        template = '%s/common/cards/review_card.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Review Card"


class CardsEntry(EntryBlock):
    amp_scripts = ['carousel']
    theme_reverse = ThemeChoiceBlock(required=False)
    theme_content = ThemeChoiceBlock(required=False)
    carousel = blocks.BooleanBlock(required=False)
    cards = blocks.StreamBlock(
        [
            ('custom', CustomCard()),
            ('person', PersonCard()),
            ('review', ReviewCard()),
            ('stream', StreamCard()),
        ],
        min_num=1
    )

    def mock(self, stop=None, carousel=True, *args, **kwargs):
        if 'theme' in kwargs:
            icon = self.SVG_ICON_LIGHT if kwargs['theme'] == constants.THEME_LIGHT \
                else self.SVG_ICON_SPACE
            file = self.SVG_SQUARE_LIGHT if kwargs['theme'] == constants.THEME_LIGHT \
                else self.SVG_SQUARE_SPACE

        else:
            icon = self.SVG_ICON_SPACE
            file = self.SVG_SQUARE_SPACE
        ret = {
            'type': 'cards',
            'value': {
                'cards': [],
                'carousel': carousel
            }
        }
        cci = {
            'text': {
                'value': self.xs,
                'align': 'center'
            },
            'button': self.button(constants.BUTTON_SECONDARY)
        }
        if self.random_counter % 2:
            cci['media'] = [{
                'type': 'svg',
                'value': {
                    'file': self.file(file).id,
                    'size': 'full'
                },
            }]
        else:
            cci['icon'] = {
                'file': self.file(icon).id,
                'size': 'l'
            }
        card_custom = [cci, cci, cci, cci, cci, cci, cci]
        i = 0
        for card_item in card_custom:
            if not carousel and stop and i == stop:
                break
            ret['value']['cards'].append({
                'type': 'custom',
                'value': {
                    'custom': card_item
                }
            })
            ret['value']['cards'][i]['value'] = card_item
            i += 1
        self.mock_data.update(ret)
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/cards.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Cards"
        icon = 'grip'
