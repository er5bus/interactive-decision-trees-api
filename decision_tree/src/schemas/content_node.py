from .. import models, ma
from .base_node import BaseNodeSchema
from ._fields import EscapedStr
from ._behaviors import BaseSchema, TimestampMixin, UniqueIdMixin
from marshmallow.validate import Length, Range, ContainsOnly, OneOf
from marshmallow import validates_schema, ValidationError, EXCLUDE, pre_load, post_dump


class ActionValueSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.ActionValue

    value = ma.Int()
    score = ma.Nested("src.schemas.tree.ScoreSchema", load_only=True, only=("id", ))
    score_dump = ma.Nested("src.schemas.tree.ScoreSchema", dump_only=True, data_key="score", attribute="score")

    class Meta:
        load_only=("score",)
        dump_only=("score_dump",)

    @pre_load
    def load_action_values(self, data, many, **kwargs):
        self.set_field_value(data, "score", { "id": self.get_field_value(data, "score")["id"] })
        return data


class ActionSchema(BaseSchema, UniqueIdMixin):
    __model__ = models.Action

    name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    order = ma.Int(required=True)

    point_to_type =  ma.String(required=True, validate=OneOf( models.PointTo.names() ))
    point_to_node = ma.Nested("src.schemas.base_node.BaseNodeSchema", only=( "id", ), allow_none=True)
    point_to_node_dump = ma.Nested("src.schemas.base_node.BaseNodeSchema", data_key="point_to_node", attribute="point_to_node")

    point_to_tree = ma.Nested("src.schemas.tree.TreeSchema", only=( "id", ), load_only=True, allow_none=True)
    point_to_tree_dump = ma.Nested("src.schemas.tree.TreeSchema", data_key="point_to_tree", attribute="point_to_tree")

    values = ma.List(ma.Nested(ActionValueSchema))

    score = ma.Nested("src.schemas.tree.ScoreSchema", only=("id", ))
    score_dump = ma.Nested("src.schemas.tree.ScoreSchema", data_key="score", attribute="score")

    class Meta:
        load_only=("point_to_node", "point_to_tree", "score")
        dump_only=("point_to_node_dump", "point_to_tree_dump", "score_dump")

    @pre_load
    def load_actions(self, data, many, **kwargs):
        point_to_type = self.get_field_value(data, "point_to_type")
        if point_to_type == str(models.PointTo.NOTHING):
            self.set_field_value(data, "point_to_tree", None)
            self.set_field_value(data, "point_to_node", None)
        
        if point_to_type == str(models.PointTo.LOGIC_NODE) or point_to_type == str(models.PointTo.CONTENT_NODE):
            point_to_node = self.get_field_value(data, "point_to_node")
            self.set_field_value(data, "point_to_tree", None)
            self.set_field_value(data, "point_to_node", { "id": point_to_node["id"] if point_to_node and "id" in point_to_node else None })

        if self.get_field_value(data, "point_to_type") == str(models.PointTo.TREES):
            point_to_tree = self.get_field_value(data, "point_to_tree")
            self.set_field_value(data, "point_to_node", None)
            self.set_field_value(data, "point_to_tree", { "id": point_to_tree["id"] if point_to_tree and "id" in point_to_tree else None })

        score = self.get_field_value(data, "score")
        self.set_field_value(data, "score", { "id": score["id"] if score else None })
        return data

    @post_dump
    def dump_actions(self, data, many, **kwargs):
        point_to_type = self.get_field_value(data, "point_to_type")

        if point_to_type == str(models.PointTo.NOTHING):
            self.set_field_value(data, "point_to_tree", None)
            self.set_field_value(data, "point_to_node", None)
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


class ContentNodeSchema(BaseNodeSchema):
    __model__ = models.ContentNode

    content_area = EscapedStr(max_length=5000, allow_none=True, required=False, validate=Length(max=5000))
    question = EscapedStr(max_length=1000,  allow_none=True, required=False, validate=Length(max=1000, min=1))
    actions = ma.List(ma.Nested(ActionSchema))
