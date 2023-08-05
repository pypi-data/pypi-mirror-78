import re
from django.utils.text import slugify
from django.conf import settings
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.rich_text import RichText
from wagtail.core import blocks
from wagtail.snippets.blocks import SnippetChooserBlock

from webspace.cms.blocks.mocker import Mocker
from webspace.cms import constants
from webspace.cms.amp.utils import amp_mode_active
from .choice import \
    ThemeChoiceBlock, \
    SizeChoiceBlock, \
    ContainerChoiceBlock, \
    ButtonChoiceBlock, \
    BackgroundPositionChoiceBlock

#  Add ids to headlines
__original__html__ = RichText.__html__
heading_re = r"<h(\d)[^>]*>([^<]*)</h\1>"


def add_id_attribute(match):
    n = match.group(1)
    text_content = match.group(2)
    id = slugify(text_content)
    return f'<h{n} id="titles-{id}">{text_content}</h{n}>'


def with_heading_ids(self):
    html = __original__html__(self)
    return re.sub(heading_re, add_id_attribute, html)


RichText.__html__ = with_heading_ids


class TextBlock(blocks.StructBlock):
    value = blocks.RichTextBlock(label="Text", required=False, features=settings.RICH_TEXT_FEATURES)

    class Meta:
        template = '%s/common/text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Text"


class SvgBlock(blocks.StructBlock):
    file = DocumentChooserBlock(required=False)


class SvgWithSizeBlock(SvgBlock):
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/svg.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Svg"


class ImageBlock(blocks.StructBlock):
    file = ImageChooserBlock(label="Image 500x500", required=False)


class ImageWithSizeBlock(ImageBlock):
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/picture_sizer.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Image"


class EmbedBlock(blocks.StructBlock):
    link = blocks.URLBlock(required=False)


class EmbedWithSizeBlock(EmbedBlock):
    size = SizeChoiceBlock(required=False)

    class Meta:
        template = '%s/common/embed.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Embed"


class BackgroundBlock(blocks.StructBlock):
    desktop = SvgBlock()
    mobile = SvgBlock()


class LinkBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=False)
    link = blocks.URLBlock(required=False, label="Button link")
    page = blocks.PageChooserBlock(required=False, label="Button Page")
    open_new_tab = blocks.BooleanBlock(default=False, required=False, label="Button nouvel onglet")

    class Meta:
        template = '%s/common/link.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Link"


class ButtonBlock(LinkBlock):
    type = ButtonChoiceBlock(required=False, label="Button type")

    class Meta:
        template = '%s/common/button.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Button"


class ButtonsBlock(blocks.StreamBlock):
    button = ButtonBlock()

    class Meta:
        template = '%s/common/buttons.html' % constants.BLOCK_TEMPLATES_PATH
        required = True


class IconTextBlock(blocks.StructBlock):
    icon = SnippetChooserBlock('cms.IconSnippet', required=True)
    text = TextBlock()

    class Meta:
        template = '%s/common/icon_text.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Icon Text"


class FormBlock(blocks.StructBlock):
    form = SnippetChooserBlock('cms.Form', required=True)

    class Meta:
        template = '%s/common/form.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Form"


class GalleryBlock(blocks.StructBlock):
    gallery = SnippetChooserBlock('cms.Gallery', required=True)

    class Meta:
        template = '%s/common/gallery.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Gallery"


class GallerySliderBlock(GalleryBlock):

    class Meta:
        template = '%s/common/gallery_slider.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Gallery Slider"


class PersonBlock(blocks.StructBlock):
    person = SnippetChooserBlock('cms.Person', required=True)

    class Meta:
        template = '%s/common/cards/person.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Person"


class EntryBlock(Mocker, blocks.StructBlock):
    bg_desktop = blocks.StreamBlock(
        [
            ('image', ImageChooserBlock()),
            ('svg', DocumentChooserBlock()),
        ],
        max_num=5,
        required=False
    )
    bg_mobile = blocks.StreamBlock(
        [
            ('image', ImageChooserBlock()),
            ('svg', DocumentChooserBlock()),
        ],
        max_num=5,
        required=False
    )
    svg_bg_position = BackgroundPositionChoiceBlock(
        required=False,
        default=constants.BACKROUND_POSITION_CENTER,
        label="Bg Position"
    )
    bg_layer = blocks.BooleanBlock(default=False, required=False)
    container = ContainerChoiceBlock(required=False)
    padding_top = blocks.BooleanBlock(default=True, required=False)
    padding_bottom = blocks.BooleanBlock(default=True, required=False)
    theme = ThemeChoiceBlock(required=False)

    def get_template(self, context=None):
        if amp_mode_active():
            return self.meta.template.replace('.html', '_amp.html')
        return self.meta.template
