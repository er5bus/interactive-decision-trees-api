from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo)
from .behaviors import UniqueIdMixin, UserMixin, TimestampMixin


class User(StructuredNode, UniqueIdMixin, UserMixin, TimestampMixin):
    full_name = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get("password"):
            self.password = kwargs.get("password", None)
