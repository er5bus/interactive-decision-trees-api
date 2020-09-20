class CypherQueryBuilder:
    """
    Cypher Query Builder
    """

    def __init__(self, cypher_func):
        self.cypher_query = ""
        self.cypher = cypher_func

    def cypher_query_builder(self, alias = "a"):
        self.cypher_query = "MATCH ({alias}) WHERE id({alias})".format(alias=alias) + "={self} "
        return self

    def return_alias(self, alias, attr=None):
        self.cypher_query += " RETURN {0}".format(alias)
        if attr:
            self.cypher_query += ".{0}".format(attr)
        return self

    def match(self, from_alias, relationship, to_alias):
        self.cypher_query += " MATCH ({0})-[:{1}]->({2})".format(from_alias, relationship, to_alias)
        return self

    def and_where(self, alias, **kwargs):
        self.cypher_query += self.where(alias, "AND", **kwargs)
        return self

    def or_where(self, alias, **kwargs):
        self.cypher_query += self.where(alias, "OR", **kwargs)
        return self

    def where(self, alias, operator, **kwargs):
        cypher_query = ""
        for attr, value in kwargs.items():
            cypher_query += operator if cypher_query else "WHERE "
            cypher_query += " {alias}.{attr} = '{value}'".format(alias=alias, attr=attr, value=value)
        return cypher_query

    def paginate(self, skip, limit):
        if skip is not None and limit is not None:
            self.cypher_query += " SKIP {skip} LIMIT {limit}".format(skip=skip, limit=limit)
        return self

    def get_one_or_none(self, func):
        try:
            results, columns = self.cypher(self.cypher_query)
            return func(results[0][0])
        except IndexError:
            return None

    def get_all(self, func):
        results, columns = self.cypher(self.cypher_query)
        items = []
        for row in results:
            item = func(row[0])
            item.load_relations = True
            items.append(item)
        return items

