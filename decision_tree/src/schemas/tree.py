from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, UniqueIdMixin, TimestampMixin
from marshmallow.validate import Length, OneOf
from marshmallow import post_dump


class ScoreSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Score

    name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    description = EscapedStr(max_length=500, required=True, validate=Length(max=500, min=4))


class TagSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Tag

    name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    description = EscapedStr(max_length=500, required=True, validate=Length(max=500, min=4))
    color = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))


class TreeSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__ = models.Tree

    tree_name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    description = EscapedStr(max_length=500, required=True, validate=Length(max=500, min=2))
    display_style = ma.String(required=True, validate=OneOf(models.Tree.DISPLAY_STYLES))

    scores = ma.Nested("ScoreSchema", many=True)

    first_node = ma.Nested("app.schemas.content_node.ContentNodeSchema")
    last_node = ma.Nested("app.schemas.content_node.ContentNodeSchema")
    tags = ma.Pluck(TagSchema, "id", many=True)

    class Meta:
        dump_only=('first_node', 'last_node' )

    @post_dump
    def node_dump(self, data, many, **kwargs):
        if "first_node" in data and data["first_node"] and "id" not in data["first_node"]:
            data["first_node"] = None
        if "last_node" in data and data["last_node"] and "id" not in data["last_node"]:
            data["last_node"] = None
        return data
