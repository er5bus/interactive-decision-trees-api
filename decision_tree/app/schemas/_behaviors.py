from .. import ma
from flask import Markup
from marshmallow import pre_load, post_load, post_dump
from collections import Iterable
from functools import partialmethod


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


class EscapedStr(ma.Field):

    def deserialize(self, value, attr = None, data = None, **kwargs):
        field_content = super().deserialize(value, attr, data, **kwargs)
        return Markup.escape(field_content) if isinstance(field_content, str) else field_content

    def serialize(self, value, *args, **kwargs):
        field_content = super().serialize(value, *args, **kwargs)
        return Markup.unescape(field_content)


class BaseSchema(ma.Schema):
    __model__ = None

    @post_load()
    def deserialize(self, data = dict(), **kwargs):
        instance = self.__model__() if data else None
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
