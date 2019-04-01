import warnings

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise

from .compat import json


class JSONDecoder(json.JSONDecoder):
    pass


class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        # Handle strings marked for translation
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(JSONEncoder, self).default(obj)
