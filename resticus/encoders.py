import warnings

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
import types

from django.utils.functional import Promise

from .compat import json
from .iterators import iterlist


class JSONDecoder(json.JSONDecoder):
    pass


class JSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, types.GeneratorType):
            return iterlist(obj)
        return super().default(obj)
