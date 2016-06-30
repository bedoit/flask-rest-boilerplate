# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports
from flask import jsonify
from flask.views import MethodView

# Third-party app imports

from flask_jwt import jwt_required, current_identity

# Imports from your apps

from .rest_schema import UserSchema


__all__ = (
    'ProfileView',
)


class ProfileView(MethodView):
    @jwt_required()
    def get(self):
        user_schema = UserSchema()
        return jsonify(user_schema.dump(current_identity).data)
