# -*- coding: utf-8 -*-

# Stdlib imports
from functools import wraps

# Core Flask imports

# Third-party app imports
from flask.ext.jwt import current_user
from flask_jwt import JWTError

# Imports from your apps


def role_required(roles=[]):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.role not in roles:
                raise JWTError('Invalid JWT header', 'Permission denied')
            return fn(*args, **kwargs)
        return decorator
    return wrapper
