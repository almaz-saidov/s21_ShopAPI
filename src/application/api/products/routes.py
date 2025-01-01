from flask import jsonify, request

from application.models import Product
from . import bp


@bp.get('/product_get')
def product_get():
    return jsonify({'product': 'works'})
