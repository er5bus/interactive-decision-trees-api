from neomodel import StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from ._behaviors import BaseStructuredNode
from ._fields import LazyLoadingRelationship
from .base_node import BaseNode


class Rule(BaseStructuredNode):
    OPERATORS = {"=": "Equal", "!=": "NotEqual", ">": "GreaterThan", "<": "LessThan", ">=": "GreaterThanOrEqual", "=<": "LessThanOrEqual"}
    operator = StringProperty(choices=OPERATORS)
    value = IntegerProperty()

    point_to_type = StringProperty()
    order = IntegerProperty()

    score_rel = RelationshipTo("src.models.tree.Score", "SCORE_LOGIC")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)

    point_to_node_rel = RelationshipTo(BaseNode, "POINT_TO_NODE")
    point_to_node = LazyLoadingRelationship(relationship="point_to_node_rel", many=False)

    point_to_tree_rel = RelationshipTo("src.models.tree.Tree", "POINT_TO_TREE")
    point_to_tree = LazyLoadingRelationship(relationship="point_to_tree_rel", many=False)


class LogicNode(BaseNode):
    rules_rel = RelationshipTo(Rule, "HAS_RULE")
    rules = LazyLoadingRelationship(relationship="rules_rel", many=True, order_by="order")

    default_point_to_type = StringProperty()

    default_tree_rel = RelationshipTo("src.models.tree.Tree", "POINT_TO_TREE")
    default_tree = LazyLoadingRelationship(relationship="default_tree_rel", many=False)

    default_node_rel = RelationshipTo("BaseNode", "POINT_TO_NODE")
    default_node = LazyLoadingRelationship(relationship="default_node_rel", many=False)
