from .. import models, ma
from .base_node import BaseNodeSchema
from ._behaviors import BaseSchema, TimestampMixin, UniqueIdMixin, EscapedStr
from marshmallow.validate import Length, Range, ContainsOnly, OneOf
from marshmallow import validates_schema, ValidationError


class ActionValueSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.ActionValue

    value = ma.Int()
    score = ma.Nested("app.schemas.tree.ScoreSchema", only=( "id", "uid" ))


class ActionSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Action

    name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    order = ma.Int(required=True)

    point_to_type =  ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    point_to_node = ma.Nested("app.schemas.base_node.BaseNodeSchema", only=( "id", "uid" ))
    point_to_tree = ma.Nested("app.schemas.tree.TreeSchema", only=( "id", "uid", "first_node" ))

    values = ma.List(ma.Nested(ActionValueSchema))

    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data = {}, **kwargs):
        if "point_to_node" not in data and (data["point_to_type"] == str(models.PointTo.LOGIC_NODE) or data["point_to_type"] == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "point_to_node")

        if "point_to_tree" not in data and (data["point_to_type"] == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "point_to_tree")


class ContentNodeSchema(BaseNodeSchema):
    __model__ = models.ContentNode

    content_area = EscapedStr(max_length=5000, allow_none=True, required=False, validate=Length(max=5000))
    question = EscapedStr(max_length=1000, required=True, validate=Length(max=1000, min=1))
    actions = ma.List(ma.Nested(ActionSchema))
