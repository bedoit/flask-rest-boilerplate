#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stdlib imports
import os
from datetime import timedelta
import requests

# Core Flask imports
from flask import send_from_directory
from flask import render_template
from flask import request

# Third-party app imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from sqlalchemy.orm.exc import NoResultFound

# Imports from your apps
from init.flask_init import app
from init.database import db
from init.jwt_init import jwt

from packages.auth.rest_schema import UserSchema
from packages.auth.models import User
from packages.utils.utils import parse_json_to_object, generate_jwt_token


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


environment_variable = 'FLASK_REST_BOILERPLATE_SETTINGS'
if os.path.isfile(os.environ.get(environment_variable, '')):
    app.config.from_envvar(environment_variable, True)
else:
    app.config.from_object('settings.sample')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['BUNDLE_ERRRORS'] = True
app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
app.config['CORS_HEADERS'] = 'X-Requested-With, Content-Type'
cors = CORS(app)
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=365)


if app.config['ADMIN_ENABLED']:
    from init.admin_init import admin
    admin.init_app(app)


if app.config['DEBUG']:
    @app.route('/media/<path:path>')
    def send_js(path):
        return send_from_directory('media', path)


# Such strange contstuction needs for linter
from init.celery_init import celery as imported_celery # flake8: noqa
celery = imported_celery


def init():
    from packages.auth.urls import auth
    from packages.auth.commands import (AddUser, ChangeExpireUser, ChangeUserPassword)

    manager.add_command('add_user', AddUser)
    manager.add_command('change_expire_user', ChangeExpireUser)
    manager.add_command('change_password', ChangeUserPassword)
    app.register_blueprint(auth)

db.init_app(app)
init()
jwt.init_app(app)

@app.route('/')
def index():
    if request.args.get('code', None):
        response = requests.post(
            url='https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            data={
                'client_id': app.config['GITHUB_CLIENT_ID'],
                'client_secret': app.config['GITHUB_CLIENT_SECRET'],
                'code': request.args.get('code'),
                'redirect_uri': app.config['GITHUB_REDIRECT_URI']
            }
        )
        if response.ok:
            json_data = response.json()
            access_token =json_data['access_token']
            r = requests.get(
                'https://api.github.com/user?access_token={0}'.format(access_token),
                headers={'Accept': 'application/json'}
            )
            json_data = r.json()
            schema, errors = UserSchema().load({ 'email': json_data['email'] })
            if errors:
                return render_template(
                    'index.html',
                    errors=errors
                )
            try:
                user = User.query.filter(User.email == json_data['email']).one()
            except NoResultFound:
                user = User()
            parse_json_to_object(user, schema)
            db.session.add(user)
            db.session.commit()
            return render_template(
                'index.html',
                token=generate_jwt_token(str(user.id))
            )
    else:
        return render_template(
            'index.html',
            r_uri=app.config['GITHUB_REDIRECT_URI'],
            scope=app.config['GITHUB_SCOPE'],
            client_id=app.config['GITHUB_CLIENT_ID']
        )


if __name__ == '__main__':
    if app.config['NEED_LINT']:
        import subprocess
        subprocess.call(["flake8", "./", "--exclude", "migrations", "--ignore", "E501,E712,E711,F403,F405"])
    manager.run()
