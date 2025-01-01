from flask import Blueprint

bp = Blueprint('clients', __name__, url_prefix='/api/v1')

from . import routes
