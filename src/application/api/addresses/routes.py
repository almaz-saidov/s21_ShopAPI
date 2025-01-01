from flask import jsonify, request

from ...models import Address
from . import bp


@bp.get()
def address_get():
    return jsonify({'address': 'works'})
