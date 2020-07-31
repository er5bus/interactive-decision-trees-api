from .. import api
from ... import models, schemas
from ...views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user
from flask import request
from neomodel import match, Traversal
from . import content_node, logic_node


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


class TreeFirstNodeSetView(generics.ListCreateAPIView):
    route_path = "/tree/<string:tree_uid>/first/node/<string:node_uid>"
    route_name = "content_node_set_first_node"

    lookup_field_and_url_kwarg = { "tree": "tree_uid", "node": "node_uid" }

    schema_class = schemas.ContentNodeSchema
    decorators = [ jwt_required ]

    def filter_node(self, model_class=None, **kwargs):
        self.current_tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        if self.current_tree:
            return self.current_tree.load_tree_node(uid=kwargs.get("node"))
        return None

    def create(self, *args, **kwargs):
        content_node = self.get_node(**kwargs)
        content_node.is_first_node = True
        content_node.save()

        first_node = self.current_tree.first_node_rel.get()
        if first_node :
            first_node.is_first_node = False
            first_node.save()

        self.current_tree.first_node_rel.disconnect_all()
        self.current_tree.first_node_rel.connect(content_node)
        return self.serialize(content_node, many=False), 200


class TreeLastNodeSetView(generics.ListCreateAPIView):
    route_path = "/tree/<string:tree_uid>/last/node/<string:node_uid>"
    route_name = "content_node_set_last_node"

    lookup_field_and_url_kwarg = { "tree": "tree_uid", "node": "node_uid" }

    schema_class = schemas.ContentNodeSchema
    decorators = [ jwt_required ]

    def filter_node(self, model_class=None, **kwargs):
        self.current_tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        if self.current_tree:
            return self.current_tree.load_tree_node(uid=kwargs.get("node"))
        return None

    def create(self, *args, **kwargs):
        content_node = self.get_node(**kwargs)
        content_node.is_last_node = True
        content_node.save()

        first_node = self.current_tree.last_node_rel.get()
        if first_node :
            first_node.is_last_node = False
            first_node.save()

        self.current_tree.last_node_rel.disconnect_all()
        self.current_tree.last_node_rel.connect(content_node)
        return self.serialize(content_node, many=False), 200


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


class NodeRetrieveView(generics.RetrieveAPIView):
    route_path = "/tree/<string:tree_uid>/node/<string:node_uid>"
    route_name = "node_retrieve"

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"tree": "tree_uid" , "node": "node_uid"}

    def filter_node(self, model_class=None, **kwargs):
        self.current_tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        self.node = self.current_tree.load_tree_node(uid=kwargs.get("node"))
        self.node.load_relations = True
        if isinstance(self.node, models.ContentNode):
            self.schema_class = schemas.ContentNodeSchema
        else:
            self.schema_class = schemas.LogicNodeSchema
        return self.node

    def retrieve(self, *args, **kwargs):
        response, response_code = super().retrieve(*args, **kwargs)

        return { "type": self.node.__class__.__name__, "display_style": self.current_tree.display_style, **response }, response_code


utils.add_url_rule(api, TreeFirstNodeSetView, TreeNodesListView, TreeLastNodeSetView, NodesRetriveView, NodeRetrieveView)
