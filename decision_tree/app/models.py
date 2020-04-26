from neomodel import (StructuredNode, StructuredRel, cardinality, BooleanProperty, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)
from .model_behaviors import UniqueIdMixin, UserMixin, TimestampMixin, LazyLoadingRelationship, BaseStructuredNode


class BaseNode(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    node_name = StringProperty(index=True)
    tree_rel = RelationshipTo("Tree", "RELATED_TO")

    @classmethod
    def inflate_node(cls, node):
        if "ContentNode" in node.labels:
            return ContentNode.inflate(node)
        elif "LogicNode" in node.labels:
            return LogicNode.inflate(node)


class Tag(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()

    tree_rel = RelationshipFrom("Tree", "HAS_TAG")
    tree = LazyLoadingRelationship(relationship="tree_rel", many=False)

    owner_rel = RelationshipTo("User", "CREATED_BY")
    owner = LazyLoadingRelationship(relationship="owner_rel", many=False)


class Score(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()

    tree_rel = RelationshipFrom("Tree", "HAS_SCORE")
    tree = LazyLoadingRelationship(relationship="tree_rel", many=False)


class Rule(BaseStructuredNode):
    OPERATORS = {"=": "Equal", "!=": "NotEqual", ">": "GreaterThan", "<": "LessThan", ">=": "GreaterThanOrEqual", "=<": "LessThanOrEqual"}
    operator = StringProperty(choices=OPERATORS)
    value = IntegerProperty()

    score_rel = RelationshipTo("Score", "SCORE_LOGIC")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)

    point_to_rel = RelationshipTo("BaseNode", "POINT_TO")
    point_to = LazyLoadingRelationship(relationship="point_to_rel", many=False)


class LogicNode(BaseNode):
    rules_rel = RelationshipTo(Rule, "HAS_RULE")
    rules = LazyLoadingRelationship(relationship="rules_rel", many=True)

    default_node_rel = RelationshipTo("BaseNode", "POINT_TO")
    default_node = LazyLoadingRelationship(relationship="default_node_rel", many=False)


class ContentNode(BaseNode):
    content_area = StringProperty()
    question = StringProperty(index=True)

    actions_rel = RelationshipTo("Action", "ACTIONS")
    actions = LazyLoadingRelationship(relationship="actions_rel")


class ActionValue(BaseStructuredNode):
    value = StringProperty()

    score_rel = RelationshipTo("Score", "SCORE_VALUE")
    score = LazyLoadingRelationship(relationship="score_rel", many=False)


class Action(BaseStructuredNode):
    name = StringProperty()

    point_to_rel = RelationshipTo("BaseNode", "POINT_TO")
    point_to = LazyLoadingRelationship(relationship="point_to_rel", many=False)

    values_rel = RelationshipTo("ActionValue", "ACTION_VALUE")
    values = LazyLoadingRelationship(relationship="values_rel")


class Tree(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    DISPLAY_STYLES = {"BUTTON": "BUTTON", "PANEL": "PANEL"}

    tree_name = StringProperty(index=True)
    description = StringProperty()
    display_style = StringProperty(choices=DISPLAY_STYLES)

    owner_rel = RelationshipTo("User", "OWNED_BY")
    owner = LazyLoadingRelationship(relationship="owner_rel", many=False)

    scores_rel = RelationshipTo("Score", "HAS_SCORE")
    scores = LazyLoadingRelationship(relationship="scores_rel")

    tags_rel = RelationshipTo("Tag", "HAS_TAG")
    tree_tags = LazyLoadingRelationship(relationship="tags_rel")
    tags = []

    tree_nodes_rel = RelationshipFrom("BaseNode", "RELATED_TO")
    logic_nodes = LazyLoadingRelationship()
    content_nodes = LazyLoadingRelationship()

    first_node_rel = RelationshipTo("ContentNode", "START_NODE")
    first_node = LazyLoadingRelationship("first_node_rel", many=False)

    def load_tree_nodes(self, skip, limit, **kwargs):
        results = self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").paginate(skip, limit).get_all(BaseNode.inflate_node)

        for node in results:
            if isinstance(node, ContentNode):
                self.content_nodes.append(node)
            elif isinstance(node, LogicNode):
                self.logic_nodes.append(node)

    def load_tree_node(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").get_one_or_none(BaseNode.inflate_node)

    def fetch_all_tree_nodes(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").get_all(BaseNode.inflate_node)

    def fetch_all_tree_scores(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("a", "HAS_SCORE", "s").return_alias("s").get_all(Score.inflate)


class User(BaseStructuredNode, UniqueIdMixin, UserMixin, TimestampMixin):
    full_name = StringProperty()

    trees_rel = RelationshipFrom("Tree", "OWNED_BY")
    trees = LazyLoadingRelationship(relationship="trees_rel")

    tags_rel = RelationshipFrom("Tag", "CREATED_BY")
    tags = LazyLoadingRelationship(relationship="tags_rel")

    def load_trees(self, skip=None, limit=None, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("t", "OWNED_BY", "a").and_where("t", **kwargs)\
            .return_alias("t").paginate(skip, limit).get_all(Tree.inflate)

    def load_tags(self, skip=None, limit=None, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("t", "CREATED_BY", "a").and_where("t", **kwargs)\
            .return_alias("t").paginate(skip, limit).get_all(Tag.inflate)
