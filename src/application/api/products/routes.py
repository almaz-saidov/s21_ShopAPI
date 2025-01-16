from datetime import date

from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.dto.product import ProductDTO
from application.models import Product
from application.schemas import ProductSchema
from application.repositories.product import ProductRepository
from . import bp

product_repository = ProductRepository()


@bp.post('/products')
def add_product():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
    
    try:
        request_data = request.json
        product_schema = ProductSchema(**request_data)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        new_product = Product(
            name=product_schema.name,
            category=product_schema.category,
            price=product_schema.price,
            available_stock=product_schema.available_stock,
            last_update_date=date.today(),
            supplier_id=product_schema.supplier_id,
            image_id=product_schema.image_id
        )
        product_dto = ProductDTO(new_product)
        product_repository.add_product(new_product)
        return jsonify({'new product': product_dto.map_product_dto_to_json()}), 201


@bp.delete('/products')
def delete_product():    
    try:
        product_id = int(request.args.get('product_id', default=None))
        
        if not product_id:
            return jsonify({'message': 'Request must contain query parameter: product_id'}), 400
        
        product_repository.delete_product(product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return '', 204


@bp.get('/all-available-products')
def get_all_available_products():
    try:
        all_available_products = product_repository.get_all_available_products()
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'all available products': [ProductDTO(product).map_product_dto_to_json() for product in all_available_products]}), 200


@bp.get('/products')
def get_product_by_id():
    try:
        product_id = int(request.args.get('product_id', default=None))
        
        if not product_id:
            return jsonify({'message': 'Request must contain query parameter: product_id'}), 400
        
        product = product_repository.get_product_by_id(product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'product': ProductDTO(product).map_product_dto_to_json()}), 200


@bp.patch('/products')
def reduce_product():
    try:
        product_id = int(request.args.get('product_id', default=None))
        reduce_by = int(request.args.get('reduce_by', default=None))
        
        if not product_id or not reduce_by:
            return jsonify({'message': 'Request must contain query parameters: product_id, reduce_by'}), 400
        
        reduced_product = product_repository.reduce_product(product_id, reduce_by)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'reduced product': ProductDTO(reduced_product)}), 200
