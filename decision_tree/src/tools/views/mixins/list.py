from ._base import BaseMethodMixin


class ListMixin(BaseMethodMixin):
    """
    List model objects.
    """

    def list (self, *args, **kwargs):
        (items, has_more, page) = self.paginate_nodes(**kwargs)
        return dict(items=self.serialize(items, True), has_more=has_more, page=page), 200


