from neomodel import StringProperty, RelationshipTo, RelationshipFrom
from ._behaviors import UniqueIdMixin, TimestampMixin, LazyLoadingRelationship, BaseStructuredNode
from .base_node import BaseNode


class Score(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()

    tree_rel = RelationshipFrom("Tree", "HAS_SCORE")
    tree = LazyLoadingRelationship(relationship="tree_rel", many=False)


class Tag(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    name = StringProperty(index=True)
    description = StringProperty()
    color = StringProperty()

    tree_rel = RelationshipFrom("Tree", "HAS_TAG")
    tree = LazyLoadingRelationship(relationship="tree_rel", many=False)

    owner_rel = RelationshipTo("app.models.user.User", "CREATED_BY")
    owner = LazyLoadingRelationship(relationship="owner_rel", many=False)


class Tree(BaseStructuredNode, UniqueIdMixin, TimestampMixin):
    DISPLAY_STYLES = {"BUTTON": "BUTTON", "PANEL": "PANEL"}

    tree_name = StringProperty(index=True)
    description = StringProperty()
    display_style = StringProperty(choices=DISPLAY_STYLES)

    owner_rel = RelationshipTo("app.models.user.User", "OWNED_BY")
    owner = LazyLoadingRelationship(relationship="owner_rel", many=False)

    scores_rel = RelationshipTo("Score", "HAS_SCORE")
    scores = LazyLoadingRelationship(relationship="scores_rel")

    tags_rel = RelationshipTo("Tag", "HAS_TAG")
    tags = LazyLoadingRelationship(relationship="tags_rel")

    tree_nodes_rel = RelationshipFrom("app.models.base_node.BaseNode", "RELATED_TO")

    first_node_rel = RelationshipTo("app.models.content_node.ContentNode", "START_NODE")
    first_node = LazyLoadingRelationship("first_node_rel", many=False)

    def load_tree_nodes(self, skip, limit, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").paginate(skip, limit).get_all(BaseNode.inflate_node)

    def load_tree_node(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").get_one_or_none(BaseNode.inflate_node)

    def fetch_all_tree_nodes(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("n", "RELATED_TO", "a").and_where("n", **kwargs)\
            .return_alias("n").get_all(BaseNode.inflate_node)

    def fetch_all_tree_scores(self, **kwargs):
        return self.cypher_query.cypher_query_builder("a").match("a", "HAS_SCORE", "s").return_alias("s").get_all(Score.inflate)
