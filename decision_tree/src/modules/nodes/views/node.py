from .... import models, schemas
from ....tools.views import generics
from flask_jwt_extended import jwt_required


class NodeRetrieveView(generics.RetrieveAPIView):
    route_path = "/tree/<string:tree_uid>/node/<string:node_uid>"
    route_name = "node_retrieve"

    #decorators = [ jwt_required ]

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
