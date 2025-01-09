from flask import Blueprint

bp = Blueprint('suppliers', __name__, url_prefix='/api')

from . import routes
