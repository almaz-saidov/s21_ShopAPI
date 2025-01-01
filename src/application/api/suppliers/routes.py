from flask import jsonify, request

from application.models import Supplier
from . import bp


@bp.get('/supplier_get')
def supplier_get():
    return jsonify({'supplier': 'works'})
