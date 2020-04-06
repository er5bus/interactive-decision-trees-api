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


class TreeSchema(schema_behaviors.BaseSchema, schema_behaviors.UniqueIdMixin, schema_behaviors.TimestampMixin):
    __model__ = models.Tree
    __relationship__ = ("scores", "owner")

    tree_name = ma.String(max_length=200, required=True, validate=Length(max=200, min=2))
    description = ma.String(max_length=500, required=True, validate=Length(max=500, min=2))
    display_style = ma.String(required=True, validate=OneOf(models.Tree.DISPLAY_STYLES))

    scores = ma.List(ma.Nested(ScoreSchema))
    #owner = ma.Nested(UserSchema)
