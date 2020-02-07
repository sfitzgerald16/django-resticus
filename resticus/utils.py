from django_filters.constants import ALL_FIELDS

try:
    # Automatic support for geospatial models
    from rest_framework_gis.filters import GeoFilterSet as FilterSet
except ImportError:
    from django_filters.filterset import FilterSet

__all__ = [
    "filterset_factory",
    "patch_form",
]


def filterset_factory(model, fields=ALL_FIELDS):
    meta = type(str("Meta"), (object,), {"model": model, "fields": fields})
    filterset = type(
        str(f"{model._meta.object_name}FilterSet"), (FilterSet,), {"Meta": meta}
    )
    return filterset


def patch_form(form):
    if form.is_bound:
        for field in list(form.fields.keys()):
            if field not in form.data and field not in form.files:
                form.fields.pop(field)
    return form
