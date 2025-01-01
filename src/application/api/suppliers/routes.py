from flask import jsonify, request

from ...models import Supplier
from . import bp


@bp.get()
def supplier_get():
    return jsonify({'supplier': 'works'})
