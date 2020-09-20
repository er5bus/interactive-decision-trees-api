from neomodel import StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from ._behaviors import BaseStructuredNode
from ._fields import LazyLoadingRelationship
from .base_node import BaseNode


class ContentNode(BaseNode):
    content_area = StringProperty()
    question = StringProperty(index=True)

    actions_rel = RelationshipTo("Action", "ACTIONS")
    actions = LazyLoadingRelationship(relationship="actions_rel", order_by="order")


class ActionValue(BaseStructuredNode):
    value = StringProperty()

    score_rel = RelationshipTo("src.models.tree.Score", "SCORE_VALUE")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)


class Action(BaseStructuredNode):
    name = StringProperty()

    order = IntegerProperty()

    point_to_type = StringProperty()

    point_to_node_rel = RelationshipTo(BaseNode, "POINT_TO_NODE")
    point_to_node = LazyLoadingRelationship(relationship="point_to_node_rel", many=False)

    point_to_tree_rel = RelationshipTo("src.models.tree.Tree", "POINT_TO_TREE")
    point_to_tree = LazyLoadingRelationship(relationship="point_to_tree_rel", many=False)

    values_rel = RelationshipTo("ActionValue", "ACTION_VALUE")
    values = LazyLoadingRelationship(relationship="values_rel")
