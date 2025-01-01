from flask import Blueprint

bp = Blueprint('images', __name__, url_prefix='/api/v1')

from . import routes
