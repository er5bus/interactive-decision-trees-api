from . import ma
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


class BaseSchema(ma.Schema):
    __model__ = None

    @post_load()
    def deserialize(self, data = dict(), **kwargs):
        instance = self.__model__() if data else None
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
