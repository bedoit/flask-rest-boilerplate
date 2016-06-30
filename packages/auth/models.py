
# -*- coding: utf-8 -*-

# Stdlib imports
import random
import string
import hashlib

# Core Flask imports

# Third-party app imports
from sqlalchemy import func

# Imports from your apps
from init.database import db, TimestampMixin, BaseModel

__all__ = (
    'User',
)


class User(BaseModel, TimestampMixin, db.Model):
    __tablename__ = 'auth_user'

    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLES = (
        ROLE_USER,
        ROLE_ADMIN
    )

    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=True)
    role = db.Column(db.String(80), default=ROLE_USER)

    allow_datetime = db.Column(
        db.DateTime, default=func.current_timestamp().op('AT TIME ZONE')('UTC'), nullable=False
    )
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def makepswd(secret):
        return hashlib.md5(secret.encode('utf-8').join('SECRET_ljas^&k12asssdgg')).hexdigest()

    def generatepswd(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))

    def __unicode__(self):
        return u'{0}'.format(self.email)
