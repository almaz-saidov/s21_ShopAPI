from flask import Blueprint

bp = Blueprint('addresses', __name__, url_prefix='/addresses')

from . import routes
