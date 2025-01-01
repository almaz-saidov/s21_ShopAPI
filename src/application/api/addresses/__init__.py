from flask import Blueprint

bp = Blueprint('addresses', __name__, url_prefix='/api/v1')

from . import routes
