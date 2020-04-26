from . import models, ma, schema_behaviors
from marshmallow import validates_schema, ValidationError, INCLUDE, EXCLUDE
from marshmallow.validate import Length, Range, ContainsOnly, OneOf


class UserSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin, schema_behaviors.TimestampMixin):
    __model__ = models.User

    full_name = ma.String(max_length=200, required=True, validate=Length(max=200, min=1))
    email = ma.String(max_length=128, required=True, validate=Length(max=128, min=1))
    password = ma.String(max_length=128, required=False, load_only=True)


class ScoreSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin):
    __model__ = models.Score

    name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=4))


class TagSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin):
    __model__ = models.Tag

    name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=4))


class TreeSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin, schema_behaviors.TimestampMixin):
    __model__ = models.Tree

    tree_name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=2))
    display_style = ma.String(required=True, validate=OneOf(models.Tree.DISPLAY_STYLES))

    scores = ma.List(ma.Nested(ScoreSchema))
    logic_nodes = ma.List(ma.Nested("LogicNodeSchema"))
    content_nodes = ma.List(ma.Nested("ContentNodeSchema"))

    first_node = ma.Nested("ContentNodeSchema", only=( "id", "uid" ))
    tags = ma.Pluck(TagSchema, "id", many=True)
    tree_tags = ma.List(ma.Nested(TagSchema), dump_only=True )


class BaseNodeSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin, schema_behaviors.TimestampMixin):
    __model__= models.BaseNode

    node_name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    #tree = ma.Nested(TreeSchema, only=( "id", "uid" ))


class ActionValueSchema(schema_behaviors.BaseSchema):
    __model__ = models.ActionValue

    value = ma.Int()
    score = ma.Nested(ScoreSchema, only=( "id", "uid" ))


class ActionSchema(schema_behaviors.BaseSchema):
    __model__ = models.Action

    name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))

    point_to = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))
    values = ma.List(ma.Nested(ActionValueSchema))


class RuleSchema(schema_behaviors.BaseSchema):
    __model__ = models.Rule

    operator = ma.String(required=True, validate=OneOf(models.Rule.OPERATORS))
    value = ma.Int()
    score = ma.Nested(ScoreSchema, only=( "id", "uid" ))
    point_to = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))


class LogicNodeSchema(BaseNodeSchema):
    __model__ = models.LogicNode

    rules = ma.List(ma.Nested(RuleSchema))
    default_node = ma.Nested(BaseNodeSchema, only=( "id", "uid" ))


class ContentNodeSchema(BaseNodeSchema):
    __model__ = models.ContentNode


    content_area = ma.String(max_length=5000, allow_none=True, required=False, validate=Length(max=5000))
    question = ma.String(max_length=1000, required=True, validate=Length(max=1000, min=1))
    actions = ma.List(ma.Nested(ActionSchema))

