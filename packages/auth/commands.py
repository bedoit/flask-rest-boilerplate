# -*- coding: utf-8 -*-

# Stdlib imports

# Core Flask imports

# Third-party app imports
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from flask_script import Command

# Imports from your apps
from init.database import db
from .models import User


__all__ = (
    'AddUser',
)


class AddUser(Command):
    def run(self):
        email = raw_input('Enter email: ')
        if User.query.filter(User.email == email).first():
            print '! User with login "{}" already exists.'.format(email)
            return

        password = raw_input('Enter password: ')
        role = raw_input('Role (admin/user, default=user): ')

        user = User(
            email=email,
            role=role or User.ROLE_USER
        )
        user.password = user.makepswd(password)
        db.session.add(user)
        db.session.commit()


class ChangeExpireUser(Command):
    def run(self):
        email = raw_input('Enter email: ')
        try:
            user = User.query.filter(User.email == email).one()
        except NoResultFound:
            print '! User with login "{}" does not exists.'.format(email)

        user.allow_datetime = func.current_timestamp().op('AT TIME ZONE')('UTC')
        db.session.add(user)
        db.session.commit()


class ChangeUserPassword(Command):
    def run(self):
        email = raw_input('Enter email: ')
        password = raw_input('Enter password: ')
        try:
            user = User.query.filter(User.email == email).one()
        except NoResultFound:
            print '! User with login "{}" does not exists.'.format(email)

        user.allow_datetime = func.current_timestamp().op('AT TIME ZONE')('UTC')
        user.password = User.makepswd(password)
        db.session.add(user)
        db.session.commit()
