from flask import jsonify, request

from application.models import Image
from . import bp


@bp.get('/images_get')
def images_get():
    return jsonify({'image': 'works'})
