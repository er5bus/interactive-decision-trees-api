from .. import api
from ... import models, schemas
from views import utils, generics
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

    route_path = "/tree/<string:id>/all/nodes"
    route_name = "tree_retrieve_nodes"

    decorators = [ jwt_required ]

    model_class = models.Tree

    def filter_node(self, model_class=None, **kwargs):
        tree = super().filter_node(model_class=model_class, **kwargs)
        if tree:
            return tree.fetch_all_tree_nodes()
        return None

    def serialize(self, tree, many=False):
        items = []
        for node in tree.fetch_all_tree_nodes():
            items.append({"value": node.id, "label": "{1}> {0} ({1})".format(node.node_name, node.__class__.__name__  ) })
        return { "items": items }


utils.add_url_rule(api, TreeNodesListView, NodesRetriveView)
