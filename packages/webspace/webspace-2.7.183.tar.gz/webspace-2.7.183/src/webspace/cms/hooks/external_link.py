from wagtail.core import hooks
from django.utils.html import escape
from wagtail.core.rich_text import LinkHandler


class NoFollowExternalLinkHandler(LinkHandler):
    identifier = 'external'

    @classmethod
    def expand_db_attributes(cls, attrs):
        href = attrs["href"]

        # Transform `rel` and `target` attribute

        target = ''
        if '/target_blank' in href:
            target = 'target="_blank"'
            href = href.replace('/target_blank', '')

        rel = 'rel="nofollow"'
        if '/rel_follow' in href:
            rel = ''
            href = href.replace('/rel_follow', '')

        return '<a href="%s" %s %s>' % (escape(href), rel, target)


@hooks.register('register_rich_text_features')
def register_external_link(features):
    features.register_link_type(NoFollowExternalLinkHandler)
