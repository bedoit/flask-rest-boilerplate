
from flask import Blueprint
from .views import *


auth = Blueprint('auth', __name__, url_prefix='/api/auth')


auth.add_url_rule('/profile',
                  view_func=ProfileView.as_view('profile_view'))
