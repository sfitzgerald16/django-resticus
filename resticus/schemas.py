import re

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.urls import URLPattern, URLResolver

from . import mixins

root_urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


class SchemaGenerator(object):
    def __init__(self, title=None, url=None, description=None, patterns=None, urlconf=None, version=None):
        if url and not url.endswith('/'):
            url += '/'

        if not urlconf:
            self.urlconf = root_urlconf
        else:
            self.urlconf = urlconf

        self.patterns = patterns
        self.title = title
        self.description = description
        self.version = version
        self.url = url

    def list_routes(self, callback, parameters):
        print('list_routes', callback, parameters)
        routes = {}
        routes_dict = {
            mixins.ListModelMixin : {
                'get': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '200': {
                            'description': 'success'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        }
                    }
                }
            },
            mixins.DetailModelMixin: {
                'get': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '200': {
                            'description': 'success'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        },
                        '404': {
                            'description': 'not found'
                        }
                    }
                }
            },
            mixins.CreateModelMixin : {
                'post': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '201': {
                            'description': 'created'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        },
                    }
                }
            },
            mixins.UpdateModelMixin : {
                'put': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '200': {
                            'description': 'success'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        }
                    }
                }
            },
            mixins.PatchModelMixin : {
                'patch': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '200': {
                            'description': 'success'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        }
                    }
                }
            },
            mixins.DeleteModelMixin : {
                'delete': {
                    'summary': '',
                    'parameters': parameters,
                    'responses': {
                        '204': {
                            'description': 'deleted'
                        },
                        '400': {
                            'description': 'error'
                        },
                        '401': {
                            'description': 'permission denied'
                        },
                        '403': {
                            'description': 'authentication required'
                        }
                    }
                }
            }
        }
        if hasattr(callback, 'view_class'):
            for item in callback.view_class.__mro__:
                if routes_dict.get(item):
                    routes.update(routes_dict[item])
        return routes


    def list_urls(self, urls, paths=None, prefix=None, count=0):
        if paths is None:
            paths = {}

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
                urlstring = prefix + simplify_regex(str(p.pattern))
                parameters = []
                params_list = re.findall('<(.*?)>', urlstring, re.DOTALL)
                for param in params_list:
                    parameters.append({'name': param, 'in': 'path', 'description': param, 'required': True, 'type': 'uuid', 'format': 'uuid'})
                path = {urlstring: self.list_routes(p.callback, parameters)}
                paths.update(path)

            elif isinstance(p, URLResolver):
                self.list_urls(p, paths=paths, prefix=prefix)

        return paths

    def get_paths(self):
        paths = self.list_urls(self.urlconf)
        # print(*paths, sep="\n")
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