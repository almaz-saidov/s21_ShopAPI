import uuid

from flask import jsonify, request, Response
from werkzeug.exceptions import NotFound

from application.schemas import ImageSchema
from application.queries.orm.image import ImageORM
from . import bp


@bp.post('/images')
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
    

@bp.delete('/images')
def delete_image():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        image_id = uuid.UUID(request.args.get('image_id', default=None))
        if not image_id:
            return jsonify({'message': 'Request must contain query parameter: image_id'}), 400
        ImageORM.delete_image(image_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return '', 204


@bp.get('/images')
def get_image_by_id():
    try:
        image_id = uuid.UUID(request.args.get('image_id', default=None))
        if not image_id:
            return jsonify({'message': 'Request must contain query parameter: image_id'}), 400
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


@bp.get('/images')
def get_image_by_product_id():
    try:
        product_id = int(request.args.get('product_id', default=None))
        if not product_id:
            return jsonify({'message': 'Request must contain query parameter: product_id'}), 400
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


@bp.patch('/images')
def change_image():
    if not request.data:
        return jsonify({'message': 'Request body must contain image byte array'}), 400

    try:
        image_id = uuid.UUID(request.args.get('image_id'))
        if not image_id:
            return jsonify({'message': 'Request must contain query parameter: image_id'}), 400
        request_data = request.data
        image_schema = ImageSchema(data=request_data)
        ImageORM.change_image(image_id, image_schema.data)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return '', 204
