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
        # self._initialise_endpoints()

        # paths = self.get_paths(None if public else request)
        # if not paths:
        #     return None

        schema = {
            'openapi': '3.0.2',
            'info': self.get_info(),
            'paths': None,
        }

        return schema
