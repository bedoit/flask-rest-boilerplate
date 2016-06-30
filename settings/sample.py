# -*- coding: utf-8 -*-
import os
from datetime import timedelta

DEBUG = True
NEED_LINT = True
ADMIN_ENABLED = DEBUG
# SQLALCHEMY_ECHO = True

SQLALCHEMY_DATABASE_URI = "postgresql://db_user:db_password@127.0.0.1/db_name"

SECRET_KEY = '271JJgsa712jhFHFS123f6avs01271'
PORT = 5000

ADMINS = (
    ('Vladimir Pal', 'mail.vpal@gmail.com'),
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media/')

REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = ''

CELERY_BROKER_URL = 'redis://localhost:6379/0'

GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_REDIRECT_URI = 'http://127.0.0.1:5000'
GITHUB_SCOPE = 'user:email'

JWT_EXPIRATION_DELTA = timedelta(days=365)
JWT_NOT_BEFORE_DELTA = timedelta(seconds=0)
JWT_VERIFY_CLAIMS = ['signature', 'exp', 'nbf', 'iat']
JWT_REQUIRED_CLAIMS = ['exp', 'iat', 'nbf']
JWT_AUTH_HEADER_PREFIX = 'JWT'
JWT_AUTH_URL_RULE = '/api/users/auth/'
JWT_AUTH_USERNAME_KEY = 'email'
JWT_AUTH_PASSWORD_KEY = 'password'
