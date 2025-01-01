from flask import Blueprint

bp = Blueprint('products', __name__, url_prefix='/api/v1')

from . import routes
