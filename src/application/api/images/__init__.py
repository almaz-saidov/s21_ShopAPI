from flask import Blueprint

bp = Blueprint('images', __name__, url_prefix='/api')

from . import routes
