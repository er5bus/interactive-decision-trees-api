from .. import models, ma
from ._behaviors import BaseSchema, UniqueIdMixin
from ._fields import EscapedStr
from .base_node import BaseNodeSchema
from marshmallow.validate import Length, Range, ContainsOnly, OneOf
from marshmallow import validates_schema, ValidationError, pre_load, post_dump


class RuleSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Rule

    operator = ma.String(required=True, validate=OneOf(models.Operator.values() ))
    value = ma.Int()
    order = ma.Int(required=True)

    point_to_type =  ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    point_to_node = ma.Nested("src.schemas.base_node.BaseNodeSchema", only=( "id", ), allow_none=True)
    point_to_node_dump = ma.Nested("src.schemas.base_node.BaseNodeSchema", data_key="point_to_node", attribute="point_to_node")

    point_to_tree = ma.Nested("src.schemas.tree.TreeSchema", only=( "id", ), allow_none=True)
    point_to_tree_dump = ma.Nested("src.schemas.tree.TreeSchema", data_key="point_to_tree", attribute="point_to_tree")

    score = ma.Nested("src.schemas.tree.ScoreSchema", only=( "id", ))
    score_dump = ma.Nested("src.schemas.tree.ScoreSchema", data_key="score", attribute="score")

    class Meta:
        load_only=("point_to_node", "point_to_tree", "score")
        dump_only=("point_to_node_dump", "point_to_tree_dump", "score_dump" )

    @pre_load
    def load_rules(self, data, many, **kwargs):
        point_to_type = self.get_field_value(data, "point_to_type")
        if point_to_type == str(models.PointTo.NOTHING):
            self.set_field_value(data, "point_to_tree", None)
            self.set_field_value(data, "point_to_node", None)

        if  point_to_type == str(models.PointTo.LOGIC_NODE) or point_to_type == str(models.PointTo.CONTENT_NODE):
            point_to_node = self.get_field_value(data, "point_to_node")
            self.set_field_value(data, "point_to_tree", None)
            self.set_field_value(data, "point_to_node", { "id": point_to_node["id"] if point_to_node and "id" in point_to_node else None })

        if point_to_type == str(models.PointTo.TREES):
            point_to_tree = self.get_field_value(data, "point_to_tree")
            self.set_field_value(data, "point_to_node", None)
            self.set_field_value(data, "point_to_tree", { "id": point_to_tree["id"] if point_to_tree and "id" in point_to_tree else None })

        score = self.get_field_value(data, "score")
        self.set_field_value(data, "score", { "id": score["id"] if score else None })
        return data

    @post_dump
    def dump_rules(self, data, many, **kwargs):
        point_to_node = self.get_field_value(data, "point_to_node")
        point_to_type = self.get_field_value(data, "point_to_type")
        point_to_tree = self.get_field_value(data, "point_to_tree")
        if point_to_type in (str(models.PointTo.LOGIC_NODE), str(models.PointTo.CONTENT_NODE)):
            self.set_field_value(data, "point_to_tree", None)
        if point_to_type == str(models.PointTo.TREES):
            self.set_field_value(data, "point_to_node", None)
        return data


    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data = {}, **kwargs):
        point_to_node = self.get_field_value(data, "point_to_node")
        point_to_type = self.get_field_value(data, "point_to_type")
        point_to_tree = self.get_field_value(data, "point_to_tree")
        if not point_to_node and (point_to_type == str(models.PointTo.LOGIC_NODE) or point_to_type == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "point_to_node")
        if not point_to_tree and (point_to_type == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "point_to_tree")


class LogicNodeSchema(BaseNodeSchema):
    __model__ = models.LogicNode

    rules = ma.List(ma.Nested(RuleSchema))

    default_point_to_type = ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    default_node = ma.Nested(BaseNodeSchema, only=( "id", ), allow_none=True)
    default_node_dump = ma.Nested(BaseNodeSchema, data_key="default_node", attribute="default_node" )

    default_tree = ma.Nested("src.schemas.tree.TreeSchema", only=( "id", ), allow_none=True)
    default_tree_dump = ma.Nested(BaseNodeSchema, data_key="default_tree", attribute="default_tree" )

    class Meta:
        load_only=("default_node", "default_tree")
        dump_only=("default_node_dump", "default_tree_dump" )

    @pre_load
    def load_default_node(self, data, many, **kwargs):
        default_point_to_type = self.get_field_value(data, "default_point_to_type")
        if default_point_to_type == str(models.PointTo.LOGIC_NODE) or default_point_to_type == str(models.PointTo.CONTENT_NODE):
            default_node = self.get_field_value(data, "default_node")
            self.set_field_value(data, "default_tree", None)
            self.set_field_value(data, "default_node", { "id": default_node["id"] if default_node and "id" in default_node else None })

        if default_point_to_type == str(models.PointTo.TREES):
            default_tree = self.get_field_value(data, "default_tree")
            self.set_field_value(data, "default_node", None)
            self.set_field_value(data, "default_tree", { "id": default_tree["id"] if default_tree and "id" in default_tree else None })

        score = self.get_field_value(data, "score")
        self.set_field_value(data, "score", { "id": score["id"] if score else None })
        return data

    @post_dump
    def dump_default_node(self, data, many, **kwargs):
        default_point_to_type = self.get_field_value(data, "default_point_to_type")
        if default_point_to_type in (str(models.PointTo.LOGIC_NODE), str(models.PointTo.CONTENT_NODE)):
            self.set_field_value(data, "default_tree", None)
        if default_point_to_type == str(models.PointTo.TREES):
            self.set_field_value(data, "default_node", None)
        return data

    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data = {}, **kwargs):
        default_node = self.get_field_value(data, "default_node")
        default_point_to_type = self.get_field_value(data, "default_point_to_type")
        default_tree = self.get_field_value(data, "default_tree")
        if not default_node and (default_point_to_type == str(models.PointTo.LOGIC_NODE) or default_point_to_type == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "default_node")

        if not default_tree and (default_point_to_type == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "default_tree")

