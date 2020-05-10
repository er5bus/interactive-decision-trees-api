from flask import Response, request, abort, jsonify


class OptionsMixin:
    """
    CORS Preflight Mixin
    """
    access_control_allowed_headers = "Content-Type, Authorization, X-Requested-With"
    access_control_max_age = 120
    access_control_allowed_credentials = False
    access_control_exposed_headers = "*"

    def cors_preflight (self, *args, **kwargs):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers" : self.access_control_allowed_headers,
            "Access-Control-Allow-Methods": tuple(self.methods),
            "Access-Control-Max-Age": self.access_control_max_age,
            "Access-Control-Allow-Credentials": self.access_control_allowed_credentials,
            "Access-Control-Expose-Headers": self.access_control_exposed_headers,
            "Vary": "Origin"  # in case of server cache the response and the origin is not a wild card
        }
        return Response(status=204, headers=headers)
