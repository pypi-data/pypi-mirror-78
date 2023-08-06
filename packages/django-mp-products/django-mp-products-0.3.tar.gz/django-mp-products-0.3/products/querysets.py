
from django.db.models import Q, QuerySet

from modeltranslation.utils import get_translation_fields
from model_search import model_search


class ProductQuerySet(QuerySet):

    def visible(self):
        return self.filter(is_visible=True)

    def for_category(self, category):
        return self.filter(category=category)

    def search(self, query=None):

        queryset = self

        if query:
            queryset = model_search(query, queryset, (
                ['code'] +
                get_translation_fields('name') +
                get_translation_fields('description')
            ))

        return queryset

    def with_attr_values(self, value_ids):

        if value_ids:
            return self.filter(attr_values__value_option__in=value_ids)

        return self
