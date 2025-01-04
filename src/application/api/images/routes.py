import uuid

from flask import jsonify, request

from application.mappers import ImageDTO
from application.models import Image
from application.schemas import ImageSchema
from application.queries.orm.image import ImageORM
from . import bp


@bp.post('/add_image')
def add_image():
    if not request.data:
        return jsonify({'message': 'Request body must contain image byte array'}), 400

    try:
        product_id = int(request.args.get('product_id'))
        request_data = request.data
        image_schema = ImageSchema(image=request_data)
        ImageORM.add_image(image_schema.image, product_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 200
    

@bp.delete('/delete_image')
def delete_image():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
 
    try:
        image_id = uuid.UUID(request.json['image_id'])
        ImageORM.delete_image(image_id)
    except Exception as e:
        return jsonify({'message': f'{e}'})
    else:
        return jsonify({'message': 'Success'}), 200
    

@bp.get('/get_image_by_product_id')
def get_image_by_product_id():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
 
    try:
        product_id = int(request.json['product_id'])
    except Exception as e:
        return jsonify({'message': f'{e}'})
    else:
        pass
