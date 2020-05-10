from neomodel import StringProperty, RelationshipTo, RelationshipFrom
from ._behaviors import UniqueIdMixin, TimestampMixin, BaseStructuredNode


class BaseNode(BaseStructuredNode, UniqueIdMixin, TimestampMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_type = self.__class__.__name__

    node_name = StringProperty(index=True)
    tree_rel = RelationshipTo("app.models.user.Tree", "RELATED_TO")

    @classmethod
    def inflate_node(cls, node):
        for cls in BaseNode.__subclasses__():
            if cls.__name__ in node.labels:
                return cls.inflate(node)
        return None
