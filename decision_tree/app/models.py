from neomodel import (StructuredNode, StructuredRel, cardinality, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)
from .model_behaviors import UniqueIdMixin, UserMixin, TimestampMixin


class User(StructuredNode, UniqueIdMixin, UserMixin, TimestampMixin):
    full_name = StringProperty()
    trees = RelationshipFrom("Tree", "OWNED_BY")


class Tree(StructuredNode, UniqueIdMixin, TimestampMixin):
    DISPLAY_STYLES = {"BUTTON": "BUTTON", "PANEL": "PANEL"}

    tree_name = StringProperty(unique_index=True)
    description = StringProperty()
    display_style = StringProperty(choices=DISPLAY_STYLES)
    owner = RelationshipTo(User, "OWNED_BY")
    scores = RelationshipTo("Score", "HAS_SCORE")


class Score(StructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()
