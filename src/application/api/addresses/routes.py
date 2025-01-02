from flask import jsonify, request

from application.mappers import AddressDTO
from application.models import Address
from application.schemas import AddressSchema
from application.queries.orm.address import AddressORM
from . import bp


@bp.post('/add_address')
def add_address():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
    
    try:
        request_data = request.json
        address_schema = AddressSchema(**request_data)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        new_address = Address(
            country=address_schema.country,
            city=address_schema.city,
            street=address_schema.street
        )
        AddressORM.add_address(new_address)

    return jsonify({'message': 'Success'}), 200


@bp.get('/get_address')
def get_address():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
    
    try:
        address_id = int(request.json['address_id'])
        address = AddressORM.get_address(address_id)
    except Exception as e:
        jsonify({'message': f'{e}'}), 400
    
    return jsonify({'message': 'Success', 'address': AddressDTO(address).map_address_dto_to_json()}), 200


@bp.delete('/delete_address')
def delete_address():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400
    
    try:
        address_id = int(request.json['address_id'])
        AddressORM.delete_address(address_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400      

    return jsonify({'message': 'Success'}), 200



