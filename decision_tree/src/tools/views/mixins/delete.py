from ._base import BaseMethodMixin
from neomodel import db
from flask import Response


class DeleteMinxin(BaseMethodMixin):
    """
    Delete model instance
    """
    def destroy (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        self.perform_delete(instance)

        return Response(status=204)

    def perform_delete(self, instance):
        with db.write_transaction:
            instance.delete()
