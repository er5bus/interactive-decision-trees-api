class LazyLoadingRelationship:
    """
    A relationship descriptor that sets and returns values.
    """

    load_relations_attr = "load_relations"

    def __init__(self, relationship=None, many=True, order_by='?'):
        self.many = many
        self.rel = relationship
        self.order_by = order_by

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if hasattr(obj, self.load_relations_attr) and self.rel and getattr(obj, self.load_relations_attr):
            results = getattr(obj, self.rel).order_by(self.order_by).all()
            for node in results:
                setattr(node, self.load_relations_attr, True)
            return results if self.many else (results and results.pop())
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = list() if self.many else None
        return obj.__dict__.get(self.name)

    def __set__(self, obj, val):
        if not self.many and isinstance(val, list):
            val = val.pop()
        obj.__dict__[self.name] = val

