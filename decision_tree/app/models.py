from neomodel import (StructuredNode, StructuredRel, cardinality, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)
from .model_behaviors import UniqueIdMixin, UserMixin, TimestampMixin, RelationshipAccess, BaseStructuredNode


class BaseNode(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    node_name = StringProperty(index=True)
    tree_rel = RelationshipTo("Tree", "RELATED_TO")

    @classmethod
    def inflate_node(cls, node):
        if "ContentNode" in node.labels:
            return ContentNode.inflate(node)
        elif "LogicNode" in node.labels:
            return LogicNode.inflate(node)


class Score(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()

    tree_rel = RelationshipFrom("Tree", "HAS_SCORE")
    tree = RelationshipAccess(rel="tree_rel", many=False)


class Rule(BaseStructuredNode):
    OPERATORS = {"=": "Equal", "!=": "NotEqual", ">": "GreaterThan", "<": "LessThan", ">=": "GreaterThanOrEqual", "=<": "LessThanOrEqual"}
    operator = StringProperty(choices=OPERATORS)
    value = IntegerProperty()

    score_rel = RelationshipTo("Score", "SCORE_LOGIC")
    score = RelationshipAccess(rel="score_rel", many=False)

    point_to_rel = RelationshipTo("BaseNode", "POINT_TO")
    point_to = RelationshipAccess(rel="point_to_rel", many=False)


class LogicNode(BaseNode):
    rules_rel = RelationshipTo(Rule, "HAS_RULE")
    rules = RelationshipAccess(rel="rules_rel", many=True)

    default_node_rel = RelationshipTo("BaseNode", "POINT_TO")
    default_node = RelationshipAccess(rel="default_node_rel", many=False)


class ContentNode(BaseNode):
    content_area = StringProperty()
    question = StringProperty(index=True)

    actions_rel = RelationshipTo("Action", "ACTIONS")
    actions = RelationshipAccess(rel="actions_rel")


class ActionValue(BaseStructuredNode):
    value = StringProperty()

    score_rel = RelationshipTo("Score", "SCORE_VALUE")
    score = RelationshipAccess(rel="score_rel", many=False)


class Action(BaseStructuredNode):
    name = StringProperty()

    point_to_rel = RelationshipTo("BaseNode", "POINT_TO")
    point_to = RelationshipAccess(rel="point_to_rel", many=False)

    values_rel = RelationshipTo("ActionValue", "ACTION_VALUE")
    values = RelationshipAccess(rel="values_rel")


class Tree(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    DISPLAY_STYLES = {"BUTTON": "BUTTON", "PANEL": "PANEL"}

    tree_name = StringProperty(index=True)
    description = StringProperty()
    display_style = StringProperty(choices=DISPLAY_STYLES)

    owner_rel = RelationshipTo("User", "OWNED_BY")
    owner = RelationshipAccess(rel="owner_rel", many=False)

    scores_rel = RelationshipTo("Score", "HAS_SCORE")
    scores = RelationshipAccess(rel="scores_rel")

    tree_nodes_rel = RelationshipFrom("BaseNode", "RELATED_TO")
    logic_nodes = RelationshipAccess()
    content_nodes = RelationshipAccess()


    def load_tree_nodes(self, skip, limit):
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (n)-[:RELATED_TO]->(a) RETURN n " + "SKIP {skip} LIMIT {limit}".format(skip=skip, limit=limit))
        for row in results:
            node = BaseNode.inflate_node(row[0])
            node.load_relations = True
            if isinstance(node, ContentNode):
                node.actions = node.actions_rel.all()
                self.content_nodes.append(node)
            elif isinstance(node, LogicNode):
                self.logic_nodes.append(node)

    def load_tree_node(self, uid):
        try:
            results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (n)-[:RELATED_TO]->(a) " + "WHERE n.uid = '{uid}' RETURN n".format(uid=uid))
            return BaseNode.inflate_node(results[0][0])
        except:
            return None

    def fetch_all_tree_nodes(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (n)-[:RELATED_TO]->(a) RETURN n")
        return [BaseNode.inflate_node(row[0]) for row in results]

    def fetch_all_tree_scores(self):
        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (a)-[:HAS_SCORE]->(s) RETURN s")
        return [Score.inflate(row[0]) for row in results]


class User(BaseStructuredNode, UniqueIdMixin, UserMixin, TimestampMixin):
    full_name = StringProperty()

    trees_rel = RelationshipFrom("Tree", "OWNED_BY")
    trees = RelationshipAccess(rel="trees_rel")

    def load_trees(self, skip=None, limit=None, operator="AND", **kwargs):
        cypher = ""
        for attr, value in kwargs.items():
            cypher += operator if cypher else "WHERE "
            cypher += " t.{attr} = '{value}'".format(attr=attr, value=value)

        paginate = ""
        if skip is not None and limit is not None:
            paginate += "SKIP {skip} LIMIT {limit}".format(skip=skip, limit=limit)

        results, columns = self.cypher("MATCH (a) WHERE id(a)={self} MATCH (t)-[:OWNED_BY]->(a) " + cypher + " RETURN t " + paginate )
        nodes = []
        for row in results:
            node = Tree.inflate(row[0])
            node.load_relations = True
            nodes.append(node)
        return nodes
