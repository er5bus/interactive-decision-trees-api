from .. import models, ma
from ._behaviors import BaseSchema, UniqueIdMixin
from .base_node import BaseNodeSchema
from marshmallow.validate import Length, Range, ContainsOnly, OneOf
from marshmallow import validates_schema, ValidationError, pre_load, post_dump


class RuleSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Rule

    operator = ma.String(required=True, validate=OneOf(models.Operator.values() ))
    value = ma.Int()
    order = ma.Int(required=True)

    point_to_type =  ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    point_to_node = ma.Nested("app.schemas.base_node.BaseNodeSchema", only=( "id", ), allow_none=True)
    point_to_node_dump = ma.Nested("app.schemas.base_node.BaseNodeSchema", data_key="point_to_node", attribute="point_to_node")

    point_to_tree = ma.Nested("app.schemas.tree.TreeSchema", only=( "id", ), allow_none=True)
    point_to_tree_dump = ma.Nested("app.schemas.tree.TreeSchema", data_key="point_to_tree", attribute="point_to_tree")

    score = ma.Nested("app.schemas.tree.ScoreSchema", only=( "id", ))
    score_dump = ma.Nested("app.schemas.tree.ScoreSchema", data_key="score", attribute="score")

    class Meta:
        load_only=('point_to_node', 'point_to_tree', 'score')
        dump_only=('point_to_node_dump', 'point_to_tree_dump', 'score_dump' )

    @pre_load
    def load_rules(self, data, many, **kwargs):
        if self.get_field_value(data, "point_to_type") == str(models.PointTo.LOGIC_NODE) or self.get_field_value(data, "point_to_type") == str(models.PointTo.CONTENT_NODE):
            self.set_field_value(data, "point_to_node", { "id": self.get_field_value(data, "point_to_node")["id"] if self.get_field_value(data, "point_to_node") and "id" in self.get_field_value(data, "point_to_node") else None })

        if self.get_field_value(data, "point_to_type") == str(models.PointTo.TREES):
            self.set_field_value(data, "point_to_tree", { "id": self.get_field_value(data, "point_to_tree")["id"] if self.get_field_value(data, "point_to_tree") and "id" in self.get_field_value(data, "point_to_tree") else None })

        self.set_field_value(data, "score", { "id": self.get_field_value(data, "score")["id"] if self.get_field_value(data, "score") else None })
        return data

    @post_dump
    def dump_rules(self, data, many, **kwargs):
        if (self.get_field_value(data, "point_to_node") and "id" not in self.get_field_value(data, "point_to_node")) or (self.get_field_value(data, "point_to_type") not in (str(models.PointTo.LOGIC_NODE), str(models.PointTo.CONTENT_NODE))) :
            self.set_field_value(data, "point_to_node", None)
        if (self.get_field_value(data, "point_to_tree") and "id" not in self.get_field_value(data, "point_to_tree")) or (self.get_field_value(data, "point_to_type") != str(models.PointTo.TREES)) :
            self.set_field_value(data, "point_to_tree", None)
        return data


    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data = {}, **kwargs):
        if not self.get_field_value(data, "point_to_node") and (self.get_field_value(data, "point_to_type") == str(models.PointTo.LOGIC_NODE) or self.get_field_value(data, "point_to_type") == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "point_to_node")

        if not self.get_field_value(data, "point_to_tree") and (self.get_field_value(data, "point_to_type") == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "point_to_tree")

class LogicNodeSchema(BaseNodeSchema):
    __model__ = models.LogicNode

    rules = ma.List(ma.Nested(RuleSchema))

    default_point_to_type = ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    default_node = ma.Nested(BaseNodeSchema, only=( "id", ), allow_none=True)
    default_node_dump = ma.Nested(BaseNodeSchema, data_key="default_node", attribute="default_node" )

    default_tree = ma.Nested("app.schemas.tree.TreeSchema", only=( "id", ), allow_none=True)
    default_tree_dump = ma.Nested(BaseNodeSchema, data_key="default_tree", attribute="default_tree" )

    class Meta:
        load_only=('default_node', 'default_tree')
        dump_only=('default_node_dump', 'default_tree_dump' )

    @pre_load
    def load_default_node(self, data, many, **kwargs):
        if self.get_field_value(data, "default_point_to_type") == str(models.PointTo.LOGIC_NODE) or self.get_field_value(data, "default_point_to_type") == str(models.PointTo.CONTENT_NODE):
            self.set_field_value(data, "default_node", { "id": self.get_field_value(data, "default_node")["id"] if self.get_field_value(data, "default_node") and "id" in self.get_field_value(data, "default_node") else None })

        if self.get_field_value(data, "default_point_to_type") == str(models.PointTo.TREES):
            self.set_field_value(data, "default_tree", { "id": self.get_field_value(data, "default_tree")["id"] if self.get_field_value(data, "default_tree") and "id" in self.get_field_value(data, "default_tree") else None })

        self.set_field_value(data, "score", { "id": self.get_field_value(data, "score")["id"] if self.get_field_value(data, "score") else None })
        return data

    @post_dump
    def dump_default_node(self, data, many, **kwargs):
        if (self.get_field_value(data, "default_node") and "id" not in self.get_field_value(data, "default_node")) or (self.get_field_value(data, "default_point_to_type") not in (str(models.PointTo.LOGIC_NODE), str(models.PointTo.CONTENT_NODE))) :
            self.set_field_value(data, "default_node", None)
        if (self.get_field_value(data, "default_tree") and "id" not in self.get_field_value(data, "default_tree")) or (self.get_field_value(data, "default_point_to_type") != str(models.PointTo.TREES)) :
            self.set_field_value(data, "default_tree", None)
        return data


    @validates_schema(skip_on_field_errors=True)
    def validate_point_to(self, data = {}, **kwargs):
        if not self.get_field_value(data, "default_node") and (self.get_field_value(data, "default_point_to_type") == str(models.PointTo.LOGIC_NODE) or self.get_field_value(data, "default_point_to_type") == str(models.PointTo.CONTENT_NODE)):
            raise ValidationError("Missing data for required field.", "default_node")

        if not self.get_field_value(data, "default_tree") and (self.get_field_value(data, "default_point_to_type") == str(models.PointTo.TREES)):
            raise ValidationError("Missing data for required field.", "default_tree")

