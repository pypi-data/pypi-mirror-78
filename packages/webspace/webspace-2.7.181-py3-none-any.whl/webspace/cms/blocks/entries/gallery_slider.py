from webspace.cms import constants
from webspace.cms.blocks.common import \
    EntryBlock, \
    GallerySliderBlock


class GallerySliderEntry(EntryBlock):
    gallery = GallerySliderBlock()

    class Meta:
        template = '%s/entries/gallery_slider.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Gallery Slider"
        icon = 'image'
