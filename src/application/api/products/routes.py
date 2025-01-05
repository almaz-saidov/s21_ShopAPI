from datetime import date

from flask import jsonify, request

from application.mappers import ProductDTO
from application.models import Product
from application.schemas import ProductSchema
from application.queries.orm.product import ProductORM
from . import bp


@bp.post('/add_product')
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

    return jsonify({'message': 'Success'}), 200


@bp.delete('/delete_product')
def delete_product():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
    
    try:
        product_id = int(request.json['product_id'])
        ProductORM.delete_product(product_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 200


@bp.get('/get_all_available_products')
def get_all_available_products():
    try:
        all_available_products = ProductORM.get_all_available_products()
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        json_all_available_products = [ProductDTO(product).map_product_dto_to_json() for product in all_available_products]
        return jsonify({'message': 'Success', 'all_available_products': json_all_available_products}), 200


@bp.get('/get_product_by_id')
def get_product_by_id():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        product_id = int(request.json['product_id'])
        product = ProductORM.get_product_by_id(product_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success', 'product': ProductDTO(product).map_product_dto_to_json()}), 200


@bp.post('/reduce_product')
def reduce_product():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        product_id = int(request.json['product_id'])
        reduce_by = int(request.json['reduce_by'])
        ProductORM.reduce_product(product_id, reduce_by)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 200
