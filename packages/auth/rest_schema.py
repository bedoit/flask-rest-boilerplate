# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports

# Third-party app imports
from marshmallow import fields

# Imports from your apps
from packages.utils.utils import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Int(dump_only=True)
    email = fields.Email()
    role = fields.Str()
