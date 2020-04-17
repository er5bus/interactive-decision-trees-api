from .. import api
from ... import models, schemas
from ...views import utils, generics
from flask_jwt_extended import jwt_required, get_current_user
from flask import request
from neomodel import match, Traversal
from . import content_node, logic_node


class TreeNodesListView(generics.RetrieveAPIView):

    route_path = "/tree/<string:tree_uid>/nodes"
    route_name = "tree_list_nodes"

    lookup_field_and_url_kwarg = { "uid": "tree_uid" }

    model_class = models.Tree
    schema_class = schemas.TreeSchema

    decorators = [ jwt_required ]

    def filter_node(self, model_class=None, **kwargs):
        self.page = request.args.get("page", type=int, default=1)
        self.item_per_page = request.args.get("item_per_page", type=int, default=10)

        tree = super().filter_node(model_class=model_class, **kwargs)
        if tree:
            tree.load_tree_nodes((self.page * self.item_per_page - self.item_per_page), self.item_per_page)
        return tree

    def retrieve(self, *args, **kwargs):
        tree = self.get_node(**kwargs)
        has_more = (len(tree.logic_nodes) + len(tree.content_nodes)) == self.item_per_page

        return { "tree": self.serialize(tree), "has_more": has_more }, 200


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
            items.append({"value": node.id, "type": node.__class__.__name__, "label": "{1}> {0} ({1})".format(node.node_name, node.__class__.__name__  ) })
        return { "items": items }


class NodeRetrieveView(generics.RetrieveAPIView):
    route_path = "/tree/<string:tree_uid>/node/<string:node_uid>"
    route_name = "node_retrieve"

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"tree": "tree_uid" , "node": "node_uid"}

    def filter_node(self, model_class=None, **kwargs):
        self.current_tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        self.node = self.current_tree.load_tree_node(kwargs.get("node"))
        self.node.load_relations = True
        if isinstance(self.node, models.ContentNode):
            self.schema_class = schemas.ContentNodeSchema
        else:
            self.schema_class = schemas.LogicNodeSchema
        return self.node

    def retrieve(self, *args, **kwargs):
        response, response_code = super().retrieve(*args, **kwargs)

        return { "type": self.node.__class__.__name__, "display_style": self.current_tree.display_style, **response }, response_code


utils.add_url_rule(api, TreeNodesListView, NodesRetriveView, NodeRetrieveView)
