from ._base import BaseMethodMixin
from collections import Iterable


class RetrieveMixin(BaseMethodMixin):
    """
    Retrieve a model instance
    """

    def retrieve (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        return self.serialize(instance, isinstance(instance, Iterable)), 200
