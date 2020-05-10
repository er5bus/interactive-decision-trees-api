from neomodel import StringProperty, IntegerProperty, RelationshipFrom, RelationshipTo
from ._behaviors import LazyLoadingRelationship, BaseStructuredNode
from .base_node import BaseNode


class Rule(BaseStructuredNode):
    OPERATORS = {"=": "Equal", "!=": "NotEqual", ">": "GreaterThan", "<": "LessThan", ">=": "GreaterThanOrEqual", "=<": "LessThanOrEqual"}
    operator = StringProperty(choices=OPERATORS)
    value = IntegerProperty()

    order = IntegerProperty()

    score_rel = RelationshipTo("app.models.tree.Score", "SCORE_LOGIC")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)

    point_to_rel = RelationshipTo("BaseNode", "POINT_TO")
    point_to = LazyLoadingRelationship(relationship="point_to_rel", many=False)


class LogicNode(BaseNode):
    rules_rel = RelationshipTo(Rule, "HAS_RULE")
    rules = LazyLoadingRelationship(relationship="rules_rel", many=True, order_by="order")

    default_node_rel = RelationshipTo("BaseNode", "POINT_TO")
    default_node = LazyLoadingRelationship(relationship="default_node_rel", many=False)
