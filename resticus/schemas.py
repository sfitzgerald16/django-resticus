import re

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from django.core.exceptions import FieldDoesNotExist
from django.urls import URLPattern, URLResolver

from . import mixins

root_urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])


class SchemaGenerator(object):
    def __init__(self, title=None, description=None, prefix=None, urlconf=None, version=None):

        if not urlconf:
            self.urlconf = root_urlconf
        else:
            self.urlconf = urlconf

        self.prefix = prefix
        self.title = title
        self.description = description
        self.version = version

    def get_model_props(self, view_class):
        model = {}
        fields_dict = {
            'AutoField': 'integer',
            'BigAutoField': 'integer',
            'BigIntegerField': 'integer',
            'BinaryField': 'bytes',
            'BooleanField': 'boolean',
            'CharField': 'string',
            'DateField': 'string',
            'DateTimeField': 'string',
            'DecimalField': 'number',
            'DurationField': 'integer',
            'EmailField': 'string',
            'FileField': 'string',
            'FilePathField': 'string',
            'FloatField': 'number',
            'ImageField': 'string',
            'IntegerField': 'integer',
            'GenericIPAddressField': 'string',
            'NullBooleanField': 'boolean',
            'PositiveIntegerField': 'integer',
            'PositiveSmallIntegerField': 'integer',
            'SlugField': 'string',
            'SmallIntegerField': 'integer',
            'TextField': 'string',
            'TimeField': 'string',
            'URLField': 'string',
            'UUIDField': 'string',
        }

        if isinstance(view_class.fields, tuple):
            for field in view_class.fields:
                if isinstance(field, str):
                    try:
                        name = view_class.model._meta.get_field(field).name
                        field_type = view_class.model._meta.get_field(field).get_internal_type()
                        if fields_dict.get(field_type):
                            model.update({name:{'type': fields_dict[field_type]}})
                    except FieldDoesNotExist:
                        continue
            print('****', model)
        # return {'id': {'type': 'string'}, 'name': {'type': 'string'}, 'is_active': {'type': 'boolean'}, 'is_default': {'type': 'boolean'}, 'primary_color': {'type': 'string'}, 'header_text_color': {'type': 'string'}, 'header_text_opacity': {'type': 'integer'}, 'primary_button_color': {'type': 'string'}, 'primary_button_text_color': {'type': 'string'}, 'secondary_button_color': {'type': 'string'}, 'secondary_button_text_color': {'type': 'string'}, 'heading_text_color': {'type': 'string'}, 'text_color': {'type': 'string'}, 'app_icon': {'type': 'string'}, 'nav_icon': {'type': 'string'}, 'splash_background': {'type': 'string'}, 'splash_logo': {'type': 'string'}}
        return model
        # return {
        #     'id': {
        #         'type': 'integer',
        #     },
        #     'name': {
        #         'type': 'string'
        #     }
        # }

    def list_routes(self, callback, parameters):
        '''
        Add http methods and responses to routes
        '''
        functions = ['get', 'post', 'put', 'patch', 'delete']
        routes = {}
        responses = {}
        summary = ''

        if hasattr(callback, 'view_class'):
            for f in functions:
                if hasattr(callback.view_class, f):
                    attr = getattr(callback.view_class, f)
                    if hasattr(callback.view_class, 'model'):
                        if f == 'get' and mixins.DetailModelMixin in callback.view_class.__mro__:
                            name = getattr(callback.view_class.model, '__name__', 'object')
                            responses = {
                                '200': {
                                    'description': 'A single ' + name,
                                    'content': {
                                        'application/json': {
                                            'schema': {
                                                'type': 'object',
                                                'properties': {
                                                    'data': {
                                                        'type': 'object',
                                                        'properties': self.get_model_props(callback.view_class)
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        if hasattr(callback.view_class.model, '__name__') and attr.__doc__:
                            summary = attr.__doc__.replace(
                                'object', callback.view_class.model.__name__)
                    routes.update(
                        {
                            f:
                                {
                                    'summary': summary,
                                    'parameters': parameters,
                                    'responses': responses
                                }
                            }
                        )
        return routes

    def parse_patterns(self, patterns, paths, prefix):
        '''
        Parse through url resolvers until all url patterns have been added
        '''
        for p in patterns:
            if isinstance(p, URLPattern):
                urlstring = prefix + simplify_regex(str(p.pattern))
                urlstring = re.sub(r'//', r'/', urlstring)
                parameters = []
                params_list = re.findall('<(.*?)>', urlstring, re.DOTALL)
                for param in params_list:
                    parameters.append({'name': param, 'in': 'path', 'description': param,
                                        'required': True, 'type': 'uuid', 'format': 'uuid'})

                path_info = self.list_routes(p.callback, parameters)
                path_info.update({'description': 'test'})

                a_list = ('description', 'get', 'post',
                            'patch', 'put', 'delete')

                pi_sorted = dict([(key, path_info[key])
                                    for key in a_list if key in path_info])

                path = {urlstring: pi_sorted}
                paths.update(path)

            elif isinstance(p, URLResolver):
                self.list_urls(p, paths=paths, prefix=prefix)

            elif isinstance(p, list):
                self.parse_patterns(p, paths=paths, prefix=prefix)

    def list_urls(self, urls, paths=None, prefix=None, count=0):
        '''
        Get a list of all urls from the given urlconf and all children
        '''
        if paths is None:
            paths = {}

        if prefix is not None and hasattr(urls, "pattern"):
            prefix = prefix + simplify_regex(str(urls.pattern))
        elif not prefix:
            prefix = ''

        if hasattr(urls, 'urlpatterns'):
            patterns = urls.urlpatterns
            self.parse_patterns(patterns, paths, prefix)

        elif hasattr(urls, 'url_patterns'):
            patterns = urls.url_patterns
            self.parse_patterns(patterns, paths, prefix)

        return paths

    def get_paths(self):
        paths = self.list_urls(self.urlconf, prefix=self.prefix)
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
