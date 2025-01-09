from flask import Blueprint

bp = Blueprint('clients', __name__, url_prefix='/api')

from . import routes
