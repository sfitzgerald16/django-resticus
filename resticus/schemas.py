from django.conf import settings
from django.urls import URLPattern, URLResolver

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

    def list_urls(self, lis, acc=None):
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        if isinstance(l, URLPattern):
            yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from self.list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from self.list_urls(lis[1:], acc)

    def get_paths(self):
        paths = []
        for p in self.list_urls(urlconf.urlpatterns):
            paths.append(p)
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
