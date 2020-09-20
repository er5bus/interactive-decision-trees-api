from .. import ma
from flask import Markup
from marshmallow import pre_load, post_load, post_dump
from collections import Iterable
from functools import partialmethod
import re


class UniqueIdMixin(object):
    id = ma.Int(allow_none=True)
    uid = ma.String()

    @pre_load
    def process_id(self, data, **kwargs):
        if data.get('id') == " ":
            data['id'] = None
        return data


class TimestampMixin(object):
    created = ma.DateTime()
    updated = ma.DateTime()


class BaseSchema(ma.Schema):
    __model__ = None

    def get_field_value(self, data, field_name):
        if self.to_camelcase(field_name) in data:
            return data[self.to_camelcase(field_name)]
        elif field_name in data:
            return data[field_name]
        else:
            return None

    def set_field_value(self, data, field_name, value):
        if self.to_camelcase(field_name) in data:
            data[self.to_camelcase(field_name)] = value
        else:
            data[field_name] = value

    def to_camelcase(self, s):
        parts = iter(s.split("_"))
        return next(parts) + "".join(i.title() for i in parts)

    def to_snake_case(self, s):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = self.to_camelcase(field_obj.data_key or field_name)

    @post_load()
    def deserialize(self, data = dict(), **kwargs):
        instance = self.__model__() if data else None
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
