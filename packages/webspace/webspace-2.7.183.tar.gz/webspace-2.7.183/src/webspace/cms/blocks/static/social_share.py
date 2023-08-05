from wagtail.core.blocks import StaticBlock
from webspace.cms.blocks.mocker import Mocker

from webspace.cms import constants


class SocialShare(Mocker, StaticBlock):
    class Meta:
        template = '%s/static/social_share.html' % constants.BLOCK_TEMPLATES_PATH
        label = "Social Share"

    def mock(self, *args, **kwargs):
        self.mock_data.update({
            'type': 'social_share',
            'value': {}
        })
        return super().mock(*args, **kwargs)
