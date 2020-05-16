from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, UniqueIdMixin, TimestampMixin
from marshmallow.validate import Length, OneOf


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

    scores = ma.List(ma.Nested("ScoreSchema"))

    first_node = ma.Nested("app.schemas.content_node.ContentNodeSchema", only=( "id", "uid" ))
    tags = ma.Pluck(TagSchema, "id", many=True)
