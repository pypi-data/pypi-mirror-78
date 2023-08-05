from webspace.cms import constants
from webspace.cms.blocks.common import \
    GalleryBlock, \
    EntryBlock


class GalleryEntry(EntryBlock):
    gallery = GalleryBlock()

    def mock(self, *args, **kwargs):
        gallery = self.get_gallery(*args, **kwargs)
        self.mock_data.update({
            'type': 'gallery',
            'value': {
                'gallery': {
                    'gallery': gallery.id
                }
            }
        })
        return super().mock(*args, **kwargs)

    class Meta:
        template = '%s/entries/gallery.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Gallery"
        icon = 'image'
