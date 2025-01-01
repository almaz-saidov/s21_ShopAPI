from flask import jsonify, request

from application.models import Client
from . import bp


@bp.get('/client_get')
def client_get():
    return jsonify({'client': 'works'})
