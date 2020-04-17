

def add_url_rule (blueprint, *args):
    for ViewClass in args:
        blueprint.add_url_rule(ViewClass.route_path, view_func=ViewClass.as_view(ViewClass.route_name), methods=ViewClass.methods)
