import uuid

from flask import jsonify, request, Response
from werkzeug.exceptions import NotFound

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
        image_schema = ImageSchema(data=request_data)
        ImageORM.add_image(image_schema.data, product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 201
    

@bp.delete('/delete_image')
def delete_image():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        image_id = uuid.UUID(request.json['image_id'])
        ImageORM.delete_image(image_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 204


@bp.get('/get_image_by_id')
def get_image_by_id():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        image_id = uuid.UUID(request.json['image_id'])
        data = ImageORM.get_image_by_id(image_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        response = Response(data)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename="image.png"'
        return response, 200


@bp.get('/get_image_by_product_id')
def get_image_by_product_id():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
 
    try:
        product_id = int(request.json['product_id'])
        data = ImageORM.get_image_by_product_id(product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        response = Response(data)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename="image.png"'
        return response, 200


@bp.patch('/change_image')
def change_image():
    if not request.data:
        return jsonify({'message': 'Request body must contain image byte array'}), 400

    try:
        image_id = uuid.UUID(request.args.get('image_id'))
        request_data = request.data
        image_schema = ImageSchema(data=request_data)
        ImageORM.change_image(image_id, image_schema.data)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 204
