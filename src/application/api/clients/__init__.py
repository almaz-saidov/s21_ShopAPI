from flask import Blueprint

bp = Blueprint('clients', __name__, url_prefix='/clients')

from . import routes
