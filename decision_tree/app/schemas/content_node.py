from .. import models, ma
from .base_node import BaseNodeSchema
from ._behaviors import BaseSchema, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length, Range, ContainsOnly, OneOf


class ActionValueSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.ActionValue

    value = ma.Int()
    score = ma.Nested("app.schemas.tree.ScoreSchema", only=( "id", "uid" ))


class ActionSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Action

    name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    order = ma.Int(required=True)

    point_to = ma.Nested("app.schemas.base_node.BaseNodeSchema", only=( "id", "uid" ))

    values = ma.List(ma.Nested(ActionValueSchema))


class ContentNodeSchema(BaseNodeSchema):
    __model__ = models.ContentNode

    content_area = ma.String(max_length=5000, allow_none=True, required=False, validate=Length(max=5000))
    question = ma.String(max_length=1000, required=True, validate=Length(max=1000, min=1))
    actions = ma.List(ma.Nested(ActionSchema))
