from neomodel import StringProperty, RelationshipTo, RelationshipFrom
from ._fields import LazyLoadingRelationship
from ._behaviors import UniqueIdMixin, UserMixin, TimestampMixin, BaseStructuredNode
from .tree import Tree, Tag


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
