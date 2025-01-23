import uuid

from flask import jsonify, request, Response
from werkzeug.exceptions import NotFound

from application.dto.image import ImageDTO
from application.repositories.image import ImageRepository
from application.schemas import ImageSchema
from . import bp

image_repository = ImageRepository()


@bp.post('/images')
def add_image():
    if not request.data:
        return jsonify({'error': 'Request body must contain image byte array'}), 400

    try:
        product_id = int(request.args.get('product_id'))
        request_data = request.data
        
        image_schema = ImageSchema(data=request_data)
        image_dto = ImageDTO(data=image_schema.data)
        
        image_repository.add_image(image_dto, product_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'new image ID': image_dto.map_image_dto_to_json(), 'product ID with new image': product_id}), 201
    

@bp.delete('/images')
def delete_image():
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON'}), 400

    try:
        image_id = uuid.UUID(request.args.get('image_id', default=None))
        
        if not image_id:
            return jsonify({'error': 'Request must contain query parameter: image_id'}), 400
        
        image_repository.delete_image(image_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return '', 204


@bp.get('/images')
def get_image_by_id():
    try:
        image_id = uuid.UUID(request.args.get('image_id', default=None))
        
        if not image_id:
            return jsonify({'error': 'Request must contain query parameter: image_id'}), 400
        
        image_dto = ImageDTO(image_repository.get_image_by_id(image_id))
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        response = Response(image_dto.data)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename="image.png"'
        return response, 200


@bp.get('/images')
def get_image_by_product_id():
    try:
        product_id = int(request.args.get('product_id', default=None))
        
        if not product_id:
            return jsonify({'error': 'Request must contain query parameter: product_id'}), 400
        
        image_dto = ImageDTO(image_repository.get_image_by_product_id(product_id))
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        response = Response(image_dto.data)
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename="image.png"'
        return response, 200


@bp.patch('/images')
def change_image():
    if not request.data:
        return jsonify({'error': 'Request body must contain image byte array'}), 400

    try:
        image_id = uuid.UUID(request.args.get('image_id'))
        
        if not image_id:
            return jsonify({'error': 'Request must contain query parameter: image_id'}), 400
        
        request_data = request.data
        image_schema = ImageSchema(data=request_data)
        image_dto = ImageDTO(id=image_id, data=image_schema.data)
        image_repository.change_image(image_dto)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return '', 204
