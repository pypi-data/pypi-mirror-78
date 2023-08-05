from django.http import Http404
from wagtail.core.url_routing import RouteResult
from taggit.models import Tag
from webspace.loader import get_model


class TagMixin(object):
    #  Child must have tags and date and subpage_types

    def route(self, request, path_components):
        if path_components:
            if path_components[0] == 'tags':
                tag_slug = path_components[1]
                try:
                    tag = Tag.objects.get(slug__iexact=tag_slug)
                except Tag.DoesNotExist:
                    raise Http404
                if self.live:
                    return RouteResult(self, kwargs={"tag": tag})
                raise Http404
            else:
                path_components[0] = path_components[0]
        return super().route(request, path_components)

    @property
    def items(self):
        model_child = get_model('cms', self.subpage_types[0])
        return model_child.objects.live().descendant_of(self).order_by('-date')

    def get_context(self, request, tag=None):
        context = super().get_context(request)
        if tag:
            context['items'] = []
        else:
            context['items'] = self.items
        context['tags'] = []
        for child in self.get_children().live().specific():
            for tag_obj in child.tags.all():
                if tag_obj.name:
                    context['tags'].append(tag_obj)
                if tag and tag_obj.slug == tag.slug:
                    context['items'].append(child)

        context['tags'] = list(dict.fromkeys(context['tags']))
        if tag:
            context['items'] = list(dict.fromkeys(context['items']))

        context['current_tag'] = tag
        return context

    def serve(self, request, *args, **kwargs):
        if 'tag' not in kwargs:
            return super().serve(request)
        else:
            return super().serve(
                request,
                extra_path_file='tags/' + kwargs['tag'].slug + '/',
                *args,
                **kwargs
            )
