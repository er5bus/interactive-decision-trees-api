from .... import models, schemas
from ....tools.views import generics
from flask_jwt_extended import jwt_required, get_current_user
from flask import request


class TreeNodesListView(generics.ListAPIView):

    route_path = "/tree/<string:tree_uid>/nodes"
    route_name = "tree_list_nodes"

    lookup_field_and_url_kwarg = { "uid": "tree_uid" }

    model_class = models.Tree

    decorators = [ jwt_required ]

    def filter_nodes(self, model_class=None, start=None, offset=None, **kwargs):
        tree = super().filter_node(model_class=model_class, uid=kwargs.get("tree_uid"))
        if tree:
            return tree.load_tree_nodes(start, abs(start - offset))
        return []

    def serialize(self, data = [], many=False, schema_class=None):
        items = list()
        for node in data:
            if  isinstance(node, models.ContentNode):
                items.append(super().serialize(node, schema_class=schemas.ContentNodeSchema))
            elif isinstance(node, models.LogicNode):
                items.append(super().serialize(node, schema_class=schemas.LogicNodeSchema))
        return items


class NodesRetriveView(generics.RetrieveAPIView):

    route_path = "/tree/<string:tree_uid>/all/nodes"
    route_name = "tree_retrieve_nodes"

    decorators = [ jwt_required ]

    model_class = models.Tree

    lookup_field_and_url_kwarg = { "uid": "tree_uid" }

    def filter_node(self, model_class=None, **kwargs):
        tree = super().filter_node(model_class=model_class, **kwargs)
        if tree:
            return tree.fetch_all_tree_nodes()
        return None

    def serialize(self, tree_nodes, many=False):
        items = []
        for node in tree_nodes:
            items.append({"value": node.id, "type": node.node_type, "label": node.node_name })
        return { "items": items }
