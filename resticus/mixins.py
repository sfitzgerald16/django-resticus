from django.core.exceptions import ValidationError

from . import http
from .utils import patch_form

__all__ = ['ListModelMixin', 'DetailModelMixin', 'CreateModelMixin',
    'UpdateModelMixin', 'DeleteModelMixin']


class ListModelMixin(object):
    streaming = True

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)

        response = {
            'data': (self.serialize(obj) for obj in queryset.iterator())
        }

        if self.paginator is not None:
            response.update(
                page=self.page.number,
                count=self.paginator.count,
                pages=self.paginator.num_pages,
                has_next_page=self.page.has_next(),
                has_previous_page=self.page.has_previous()
            )
        return response


class DetailModelMixin(object):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return {'data': self.serialize(self.object)}


class CreateModelMixin(object):
    def put(self, request, *args, **kwargs):
        form = self.get_form(
            data=request.data,
            files=request.FILES
        )
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def form_valid(self, form):
        data = super(CreateModelMixin, self).form_valid(form)
        return http.Http201(data)


class UpdateModelMixin(object):
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(
            data=request.data,
            files=request.FILES,
            instance=self.object
        )
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class PatchModelMixin(object):
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(
            data=request.data,
            files=request.FILES,
            instance=self.object
        )
        form = patch_form(form)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class DeleteModelMixin(object):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as err:
            return http.Http400(err.message)
        return http.Http204()
