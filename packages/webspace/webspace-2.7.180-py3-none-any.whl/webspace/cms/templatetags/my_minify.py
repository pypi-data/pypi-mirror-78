from django.template import (Library, Node)
import json
import logging


logger = logging.getLogger('minify_schema')
register = Library()


class MinifySchema(Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        ld = self.nodelist.render(context)
        try:
            return json.dumps(json.loads(ld))
        except Exception:
            logger.error(str(ld))
            return ''


@register.tag('minify_schema')
def minify_schema(parser, token):
    nodelist = parser.parse(('endminify_schema',))
    parser.delete_first_token()
    return MinifySchema(
        nodelist,
    )
