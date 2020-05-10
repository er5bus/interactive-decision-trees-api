from neomodel import StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from ._behaviors import LazyLoadingRelationship, BaseStructuredNode
from .base_node import BaseNode


class ContentNode(BaseNode):
    content_area = StringProperty()
    question = StringProperty(index=True)

    actions_rel = RelationshipTo("Action", "ACTIONS")
    actions = LazyLoadingRelationship(relationship="actions_rel", order_by="order")


class ActionValue(BaseStructuredNode):
    value = StringProperty()

    score_rel = RelationshipTo("app.models.tree.Score", "SCORE_VALUE")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)


class Action(BaseStructuredNode):
    name = StringProperty()

    order = IntegerProperty()

    point_to_rel = RelationshipTo(BaseNode, "POINT_TO")
    point_to = LazyLoadingRelationship(relationship="point_to_rel", many=False)

    values_rel = RelationshipTo("ActionValue", "ACTION_VALUE")
    values = LazyLoadingRelationship(relationship="values_rel")
