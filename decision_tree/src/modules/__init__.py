from .auth import api as auth_blueprint
from .nodes import api as nodes_blueprint
from .trees import api as trees_blueprint


api_blueprints = [
    auth_blueprint,
    nodes_blueprint,
    trees_blueprint
]
