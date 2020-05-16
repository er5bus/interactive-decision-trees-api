from .. import models, ma
from ._behaviors import BaseSchema, UniqueIdMixin
from .base_node import BaseNodeSchema
from marshmallow.validate import Length, Range, ContainsOnly, OneOf
from marshmallow import validates_schema, ValidationError


class RuleSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Rule

    operator = ma.String(required=True, validate=OneOf(models.Operator.values() ))
    value = ma.Int()
    order = ma.Int(required=True)

    point_to_type =  ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    point_to_node = ma.Nested("app.schemas.base_node.BaseNodeSchema", only=( "id", "uid" ))
    point_to_tree = ma.Nested("app.schemas.tree.TreeSchema", only=( "id", "uid", "first_node" ))

    score = ma.Nested("app.schemas.tree.ScoreSchema", only=( "id", "uid" ))

    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data, **kwargs):
        if "point_to_node" not in data and (data["point_to_type"] == str(models.PointTo.LOGIC_NODE) or data["point_to_type"] == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "point_to_node")

        if "point_to_tree" not in data and (data["point_to_type"] == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "point_to_tree")


class LogicNodeSchema(BaseNodeSchema):
    __model__ = models.LogicNode

    rules = ma.List(ma.Nested(RuleSchema))

    default_point_to_type = ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    default_node = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))
    default_tree = ma.Nested("app.schemas.tree.TreeSchema", only=( "id", "uid", "first_node" ))

    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data, **kwargs):
        if "default_node" not in data and \
            (data["default_point_to_type"] == str(models.PointTo.LOGIC_NODE) or data["default_point_to_type"] == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "default_node")

        if "default_tree" not in data and (data["default_point_to_type"] == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "default_tree")

