from ._base import BaseMethodMixin
from copy import deepcopy
from neomodel import db
from flask import request


class UpdateMixin(BaseMethodMixin):
    """
    Update model instance
    """
    def update (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        instance_updated = self.deserialize(request.json, deepcopy(instance), partial=False)
        with db.transaction:
            self.perform_update(instance_updated)

        return self.serialize(instance_updated), 200

    def partial_update (self, *args, **kwargs):
        instance = self.get_node(**kwargs)
        instance_updated = self.deserialize(request.json ,partial=True)
        with db.transaction:
            self.perform_update(instance)

        return self.serialize(instance_updated), 200

    def perform_update(self, instance):
        instance.save()
