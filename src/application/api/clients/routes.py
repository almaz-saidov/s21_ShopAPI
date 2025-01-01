from flask import jsonify, request

from ...models import Client
from . import bp


@bp.get()
def client_get():
    return jsonify({'client': 'works'})
