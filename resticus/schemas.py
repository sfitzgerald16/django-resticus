from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.urls import URLPattern, URLResolver

from . import mixins

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


class SchemaGenerator(object):
    def __init__(self, title=None, url=None, description=None, patterns=None, urlconf=None, version=None):
        if url and not url.endswith('/'):
            url += '/'

        self.patterns = patterns
        self.urlconf = urlconf
        self.title = title
        self.description = description
        self.version = version
        self.url = url

    def list_routes(self, callback):
        routes = []
        routes_dict = {
            mixins.ListModelMixin : 'get',
            mixins.DetailModelMixin : 'get',
            mixins.CreateModelMixin : 'post',
            mixins.UpdateModelMixin : 'put',
            mixins.PatchModelMixin : 'patch',
            mixins.DeleteModelMixin : 'delete'
        }
        if hasattr(callback, 'view_class'):
            for item in callback.view_class.__mro__:
                if routes_dict.get(item):
                    routes.append({routes_dict[item]: {'summary': ''}})
        return routes


    def list_urls(self, urls, paths=None, prefix=None, count=0):
        if paths is None:
            paths = []

        if prefix is not None and hasattr(urls, "pattern"):
            prefix = prefix + simplify_regex(str(urls.pattern))
        elif not prefix:
            prefix = ''

        if hasattr(urls, 'urlpatterns'):
            patterns = urls.urlpatterns
        elif hasattr(urls, 'url_patterns'):
            patterns = urls.url_patterns

        for p in patterns:
            if isinstance(p, URLPattern):
                path = {prefix + simplify_regex(str(p.pattern)): self.list_routes(p.callback)}
                paths.append(path)

            elif isinstance(p, URLResolver):
                self.list_urls(p, paths=paths, prefix=prefix, count=count+1)

        return paths

    def get_paths(self):
        paths = self.list_urls(urlconf)
        print(*paths, sep="\n")
        return paths

    def get_info(self):
        # Title and version are required by openapi specification 3.x
        info = {
            'title': self.title or '',
            'version': self.version or ''
        }

        if self.description is not None:
            info['description'] = self.description

        return info

    def get_schema(self, request=None, public=False):
        """
        Generate a OpenAPI schema.
        """
        paths = self.get_paths()
        if not paths:
            return None

        schema = {
            'openapi': '3.0.2',
            'info': self.get_info(),
            'paths': paths,
        }

        return schema
