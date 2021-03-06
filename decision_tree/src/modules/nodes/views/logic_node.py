from .... import models, schemas
from ....tools.views import generics
from flask_jwt_extended import jwt_required, get_current_user


class LogicNodeCreateView(generics.CreateAPIView):

    route_path = "/tree/<string:tree_uid>/node/logic"
    route_name = "logic_node_create"

    model_class = models.LogicNode
    schema_class = schemas.LogicNodeSchema

    lookup_field_and_url_kwarg = { "uid": "tree_uid" }

    decorators = [ jwt_required ]

    def create(self, *args, **kwargs):
        self.current_tree = self.get_node(model_class=models.Tree, **kwargs)
        return super().create(*args, **kwargs)

    def perform_create(self, logic_node_instance):
        logic_node_instance.save()
        for rule in logic_node_instance.rules or []:
            rule.save()
            rule.score_rel.connect(rule.score)

            if rule.point_to_type == str(models.PointTo.LOGIC_NODE) or rule.point_to_type == str(models.PointTo.CONTENT_NODE):
                rule.point_to_node_rel.connect(rule.point_to_node)

            if rule.point_to_type == str(models.PointTo.TREES):
                rule.point_to_tree_rel.connect(rule.point_to_tree)

            logic_node_instance.rules_rel.connect(rule)

        if logic_node_instance.default_point_to_type == str(models.PointTo.LOGIC_NODE) or logic_node_instance.default_point_to_type == str(models.PointTo.CONTENT_NODE):
            logic_node_instance.default_node_rel.connect(logic_node_instance.default_node)

        if logic_node_instance.default_point_to_type == str(models.PointTo.TREES):
            logic_node_instance.default_tree_rel.connect(logic_node_instance.default_tree)

        logic_node_instance.tree_rel.connect(self.current_tree)


class LogicNodeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    route_path = "/tree/<string:tree_uid>/node/logic/<string:node_uid>"
    route_name = "logic_node_retrieve_update_destroy"

    model_class = models.LogicNode
    schema_class = schemas.LogicNodeSchema

    decorators = [ jwt_required ]

    lookup_field_and_url_kwarg = {"tree": "tree_uid", "node": "node_uid"}

    def filter_node(self, model_class=None, **kwargs):
        tree = models.Tree.nodes.filter(uid__exact=kwargs.get("tree")).get_or_none()
        self.logic_node = tree.load_tree_node(uid=kwargs.get("node"))
        self.logic_node.load_relations = True
        return self.logic_node

    def perform_relation_delete(self, logic_node_instance):
        for rule in logic_node_instance.rules_rel.all():
            if rule not in logic_node_instance.rules:
                rule.delete()

    def perform_update(self, logic_node_instance):
        logic_node_instance.save()
        self.perform_relation_delete(logic_node_instance)
        for rule in logic_node_instance.rules or []:
            rule.save()
            rule.score_rel.disconnect_all()

            rule.score_rel.connect(rule.score)

            rule.point_to_node_rel.disconnect_all()
            if rule.point_to_type == str(models.PointTo.LOGIC_NODE) or rule.point_to_type == str(models.PointTo.CONTENT_NODE):
                rule.point_to_node_rel.connect(rule.point_to_node)

            rule.point_to_tree_rel.disconnect_all()
            if rule.point_to_type == str(models.PointTo.TREES):
                rule.point_to_tree_rel.connect(rule.point_to_tree)

            logic_node_instance.rules_rel.connect(rule)

        if logic_node_instance.default_point_to_type == str(models.PointTo.LOGIC_NODE) or logic_node_instance.default_point_to_type == str(models.PointTo.CONTENT_NODE):
            logic_node_instance.default_node_rel.disconnect_all()
            logic_node_instance.default_node_rel.connect(logic_node_instance.default_node)

        if logic_node_instance.default_point_to_type == str(models.PointTo.TREES):
            logic_node_instance.default_tree_rel.disconnect_all()
            logic_node_instance.default_tree_rel.connect(logic_node_instance.default_tree)


    def perform_delete(self, logic_node_instance):
        self.perform_relation_delete(logic_node_instance)
        super().perform_delete(logic_node_instance)
