from neomodel import StringProperty, RelationshipTo, RelationshipFrom, BooleanProperty
from ._behaviors import UniqueIdMixin, TimestampMixin, BaseStructuredNode


class BaseNode(BaseStructuredNode, UniqueIdMixin, TimestampMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_type = self.__class__.__name__

    node_name = StringProperty(index=True)
    tree_rel = RelationshipTo("app.models.user.Tree", "RELATED_TO")

    is_last_node = BooleanProperty(default=False)
    is_first_node = BooleanProperty(default=False)

    @classmethod
    def inflate_node(cls, node):
        for cls in BaseNode.__subclasses__():
            if cls.__name__ in node.labels:
                return cls.inflate(node)
        return None
