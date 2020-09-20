from .. import models, ma
from ._fields import EscapedStr
from ._behaviors import BaseSchema, UniqueIdMixin, TimestampMixin
from marshmallow.validate import Length, Range, ContainsOnly, OneOf


class BaseNodeSchema(BaseSchema, UniqueIdMixin, TimestampMixin):
    __model__= models.BaseNode

    node_name = EscapedStr(max_length=200, data_key="name", required=True, validate=Length(max=200, min=2))
    node_type = ma.String(dump_only=True)

    is_last_node = ma.Bool()
    is_first_node = ma.Bool()
    #tree = ma.Nested(TreeSchema, only=( "id", "uid" ))

