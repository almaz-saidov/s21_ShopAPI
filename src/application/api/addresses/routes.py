from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.mappers import AddressDTO
from application.models import Address
from application.schemas import AddressSchema
from application.queries.orm.address import AddressORM
from . import bp


@bp.post('/addresses')
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
        return jsonify({'message': 'Success'}), 201


@bp.get('/addresses')
def get_address():
    try:
        address_id = request.args.get('address_id', default=None)
        if not address_id:
            return jsonify({'message': 'Request must contain query parameter: address_id'}), 400
        address = AddressORM.get_address(address_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success', 'address': AddressDTO(address).map_address_dto_to_json()}), 200


@bp.delete('/addresses')
def delete_address():
    try:
        address_id = request.args.get('address_id', default=None)
        if not address_id:
            return jsonify({'message': 'Request must contain query parameter: address ID'}), 400
        AddressORM.delete_address(address_id)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return '', 204
