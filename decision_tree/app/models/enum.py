from enum import Enum

class BaseEnum(Enum):

    @classmethod
    def values(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def names(cls):
        return list(map(lambda c: c.name, cls))


class PointTo(BaseEnum):
    LOGIC_NODE = 0
    CONTENT_NODE = 1
    TREES = 2
    NOTHING = 3

    def __str__(self):
        return str(self.name)


class Operator(BaseEnum):
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN_OR_EQUAL = "=<"
