from . import ma
from marshmallow import pre_load, post_load, post_dump
from collections import Iterable
from functools import partialmethod


class UniqueIdMixin(object):
    id = ma.Int()
    uid = ma.String()


class TimestampMixin(object):
    created = ma.DateTime()
    updated = ma.DateTime()


class BaseSchema(ma.Schema):
    __model__ = None
    __relationship__ = tuple()

    @post_load()
    def deserialize(self, data = dict(), **kwargs):
        current_instance = self.context.get("instance")
        if current_instance and isinstance(current_instance, self.__model__):
            instance = current_instance
        else:
            instance = self.__model__()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
