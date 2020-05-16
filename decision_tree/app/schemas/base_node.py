from .. import models, ma
from ._behaviors import BaseSchema, EscapedStr, UniqueIdMixin, TimestampMixin
from marshmallow.validate import Length, Range, ContainsOnly, OneOf


class BaseNodeSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__= models.BaseNode

    node_name = EscapedStr(max_length=200, required=True, validate=Length(max=200, min=2))
    node_type = ma.String(dump_only=True)
    #tree = ma.Nested(TreeSchema, only=( "id", "uid" ))

