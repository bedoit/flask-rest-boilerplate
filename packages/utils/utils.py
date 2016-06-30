from datetime import datetime
import jwt

from flask import current_app

from marshmallow import Schema, post_dump


def generate_jwt_token(user_id):
    iat = datetime.utcnow()
    return jwt.encode(
        {
            'user_id': user_id,
            'iat': iat,
            'exp':
                (iat + current_app.config.get('JWT_EXPIRATION_DELTA')),
            'nbf':
                (iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')),
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    ).decode('utf-8')


def parse_json_to_object(obj, data_json, fields=(), exclude=()):
    _fields = set(data_json.keys())

    if exclude:
        _fields = _fields - set(exclude)

    if fields:
        _fields = set(fields) & _fields

    _fields -= set(['id'])

    for field in _fields:
        value = data_json[field]
        setattr(obj, field, value)


class BaseSchema(Schema):
    @post_dump
    def remove_skip_values(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }
