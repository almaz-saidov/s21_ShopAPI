from flask import jsonify, request

from ...models import Image
from . import bp


@bp.get()
def images_get():
    return jsonify({'image': 'works'})
