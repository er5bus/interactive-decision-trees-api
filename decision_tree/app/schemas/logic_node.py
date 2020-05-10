from .. import models, ma
from ._behaviors import BaseSchema, UniqueIdMixin
from .base_node import BaseNodeSchema
from marshmallow.validate import Length, Range, ContainsOnly, OneOf


class RuleSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Rule

    operator = ma.String(required=True, validate=OneOf(models.Rule.OPERATORS))
    value = ma.Int()
    order = ma.Int(required=True)

    score = ma.Nested("app.schemas.tree.ScoreSchema", only=( "id", "uid" ))
    point_to = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))


class LogicNodeSchema(BaseNodeSchema):
    __model__ = models.LogicNode

    rules = ma.List(ma.Nested(RuleSchema))
    default_node = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))
