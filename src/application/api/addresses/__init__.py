from flask import Blueprint

bp = Blueprint('addresses', __name__, url_prefix='/api')

from . import routes
