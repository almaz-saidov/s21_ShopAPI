from flask import jsonify, request

from application.models import Address
from . import bp


@bp.get('/address_get')
def address_get():
    return jsonify({'address': 'works'})
