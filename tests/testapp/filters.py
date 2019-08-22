from resticus.filters import FilterSet

from .models import Book

__all__ = ['BookFilter']


class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {
            'author': ['exact'],
            'publisher': ['exact'],
            'price': ['exact', 'lt', 'lte', 'gt', 'gte']
        }
