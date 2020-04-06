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
        relationship_instances = dict()
        self.make_object(instance, relationship_instances, data)
        if relationship_instances:
            return instance, relationship_instances
        return instance

    def make_object(self, instance, relationship_instances, data):
        for key, value in data.items():
            if key not in self.__relationship__ :
                setattr(instance, key, value)
            else:
                relationship_instances[key] = value
