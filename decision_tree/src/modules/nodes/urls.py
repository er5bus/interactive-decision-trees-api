from . import api
from ...tools import urls

# views
from .views.content_node import ContentNodeCreateView, ContentNodeRetrieveUpdateDestroyView
from .views.logic_node import LogicNodeCreateView, LogicNodeRetrieveUpdateDestroyView
from .views.node import NodeRetrieveView
from .views.nodes import NodesRetriveView, TreeNodesListView
from .views.set_first_node import TreeFirstNodeSetView
from .views.set_last_node import TreeLastNodeSetView


urls.add_url_rule(
    api,
    ContentNodeCreateView,
    ContentNodeRetrieveUpdateDestroyView,
    LogicNodeCreateView,
    LogicNodeRetrieveUpdateDestroyView,
    NodeRetrieveView,
    NodesRetriveView,
    TreeNodesListView,
    TreeFirstNodeSetView,
    TreeLastNodeSetView
)
