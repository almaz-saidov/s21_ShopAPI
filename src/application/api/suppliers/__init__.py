from flask import Blueprint

bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

from . import routes
