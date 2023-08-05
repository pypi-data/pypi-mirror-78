import logging
import os

from django.conf import settings
from django.core.handlers.base import BaseHandler
from django.test.client import RequestFactory
from wagtail.core.models import Page

from webspace.loader import get_model
from webspace.cms.bakery.views import BuildableDetailView
from webspace.cms.bakery.abstract import WagtailPageBakeryModel
from webspace.api import API

logger = logging.getLogger('bakery')

USER_AGENT_DESKTOP = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
USER_AGENT_MOBILE = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"


class WagtailBakeryView(BuildableDetailView):

    def __init__(self, *args, **kwargs):
        self.handler = BaseHandler()
        self.handler.load_middleware()
        self.request = None
        super().__init__(*args, **kwargs)

    def get(self, request):
        response = self.handler.get_response(request)
        return response

    def get_content(self, obj):
        response = self.get(self.request)
        if hasattr(response, 'render'):
            return response.render().content
        if hasattr(response, 'content'):
            return response.content
        raise AttributeError(
            "'%s' object has no attribute 'render' or 'content'" % response)

    def get_build_path(self, obj):
        url = self.get_url(obj)
        site = self.get_site(obj)
        build_path = os.path.join(settings.BUILD_DIR, site.hostname, url[1:])
        os.path.exists(build_path) or os.makedirs(build_path)
        return os.path.join(build_path, 'index.html')

    def get_url(self, obj):
        return obj.relative_url(self.get_site(obj))

    def get_path(self, obj):
        return obj.path

    def build_object(self, obj):
        logger.debug("Building %s" % obj)

        self.build_object_env(obj)
        self.build_object_env(obj, mobile=True)
        self.build_object_env(obj, amp=True)
        self.build_object_env(obj, mobile=True, amp=True)

    def build_object_env(self, obj, amp=False, mobile=False):
        # Fix create page root
        if self.get_url(obj):
            site = self.get_site(obj)
            user_agent = USER_AGENT_MOBILE if mobile else USER_AGENT_DESKTOP
            pre_url = '/amp' if amp else ''
            url = pre_url + self.get_url(obj) + '?build=true'
            logger.debug("Building %s:%s" % (site.hostname, str(site.port) + url))
            self.request = RequestFactory(
                SERVER_NAME=site.hostname,
                SERVER_PORT=str(site.port)
            ).get(url, HTTP_USER_AGENT=user_agent)
            self.set_kwargs(obj)
            path = self.get_build_path(obj)
            if mobile:
                path = path.replace('.html', '-mobile.html')

            content = self.get_content(obj)
            if amp:
                path = path.replace('.html', '-amp.html')
                content = API.request(
                    '/amp/transform',
                    {'html': content.decode()}
                )
            self.build_file(path, content)

    def build_queryset(self):
        for item in self.get_queryset().all():
            url = self.get_url(item)
            if url is not None:
                self.build_object(item)

    def get_site(self, obj):
        return obj.get_site()

    class Meta:
        abstract = True


class AllBuildablePagesView(WagtailBakeryView):

    def get_queryset(self):
        return Page.objects.all() \
            .public() \
            .type(WagtailPageBakeryModel) \
            .live()


class BlogIndexTagPagesView(WagtailBakeryView):

    def get_site(self, obj):
        return obj.content_object.get_site()

    def get_url(self, obj):
        BlogIndexPage = get_model('cms', 'BlogIndexPage')
        site = obj.content_object.get_site()
        index_blog = BlogIndexPage.objects.in_site(site).first()
        blog_index_url = index_blog.relative_url(site)

        return '%s' % blog_index_url + 'tags/%s' % obj.tag.slug + '/'

    def get_queryset(self):
        BlogPageTag = get_model('cms', 'BlogPageTag')
        return BlogPageTag.objects.all()
