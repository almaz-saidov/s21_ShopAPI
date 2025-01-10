from datetime import date

from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.mappers import ProductDTO
from application.models import Product
from application.schemas import ProductSchema
from application.queries.orm.product import ProductORM
from . import bp


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
        ProductORM.add_product(new_product)

    return jsonify({'message': 'Success'}), 201


@bp.delete('/products')
def delete_product():    
    try:
        product_id = int(request.args.get('product_id', default=None))
        if not product_id:
            return jsonify({'message': 'Request must contain query parameter: product_id'}), 400
        ProductORM.delete_product(product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 204


@bp.get('/all-available-products')
def get_all_available_products():
    try:
        all_available_products = ProductORM.get_all_available_products()
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        json_all_available_products = [ProductDTO(product).map_product_dto_to_json() for product in all_available_products]
        return jsonify({'message': 'Success', 'all_available_products': json_all_available_products}), 200


@bp.get('/products')
def get_product_by_id():
    try:
        product_id = int(request.args.get('product_id', default=None))
        if not product_id:
            return jsonify({'message': 'Request must contain query parameter: product_id'}), 400
        product = ProductORM.get_product_by_id(product_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success', 'product': ProductDTO(product).map_product_dto_to_json()}), 200


@bp.patch('/products')
def reduce_product():
    try:
        product_id = int(request.args.get('product_id', default=None))
        reduce_by = int(request.args.get('reduce_by', default=None))
        if not product_id or not reduce_by:
            return jsonify({'message': 'Request must contain query parameters: product_id, reduce_by'}), 400
        ProductORM.reduce_product(product_id, reduce_by)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 200 # and new product
