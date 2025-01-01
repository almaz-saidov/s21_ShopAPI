from flask import jsonify, request

from ...models import Product
from . import bp


@bp.get()
def product_get():
    return jsonify({'product': 'works'})
