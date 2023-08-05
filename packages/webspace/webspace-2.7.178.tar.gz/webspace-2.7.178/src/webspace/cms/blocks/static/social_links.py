from wagtail.core.blocks import StaticBlock
from webspace.cms.blocks.mocker import Mocker

from webspace.cms import constants


class SocialLinks(Mocker, StaticBlock):
    class Meta:
        template = '%s/static/social_links.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Social Links"

    def mock(self, *args, **kwargs):
        self.mock_data.update({
            'type': 'social_links',
            'value': {}
        })
        return super().mock(*args, **kwargs)
