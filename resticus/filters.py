from django.contrib.gis import forms
from django.contrib.gis.db import models
from django.contrib.gis.db.models.fields import BaseSpatialField

from django_filters.constants import ALL_FIELDS
from django_filters import Filter, FilterSet as BaseFilterSet


# Geospatial filter functionality adapted from
# drf-gis and updated for django-filters 2.x.

class GeometryFilter(Filter):
    field_class = forms.GeometryField

    # def __init__(self, *args, **kwargs):
    #     kwargs.setdefault('widget', forms.TextInput)
    #     super().__init__(*args, **kwargs)


class PointFilter(Filter):
    field_class = forms.PointField


class FilterSet(BaseFilterSet):
    GIS_FILTER_DEFAULTS = {
        models.GeometryField: {'filter_class': GeometryFilter},
    }

    FILTER_DEFAULTS = dict(BaseFilterSet.FILTER_DEFAULTS)
    FILTER_DEFAULTS.update(GIS_FILTER_DEFAULTS)


def filterset_factory(model, fields=ALL_FIELDS):
    meta = type('Meta', (object,), {'model': model, 'fields': fields})
    filterset = type(f'{model._meta.object_name}FilterSet', (FilterSet,), {'Meta': meta})
    return filterset
