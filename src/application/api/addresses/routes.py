from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.dto.address import AddressDTO
from application.models.address import Address
from application.repositories.address import AddressRepository
from application.schemas import AddressSchema
from . import bp

address_repository = AddressRepository()


@bp.post('/addresses')
def add_address():
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    try:
        request_data = request.json
        address_schema = AddressSchema(**request_data)
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        new_address = Address(
            country=address_schema.country,
            city=address_schema.city,
            street=address_schema.street
        )
        address_dto = AddressDTO(new_address)
        new_address_dto = address_repository.add_address(address_dto)
        return jsonify({'new address': new_address_dto.map_address_dto_to_json()}), 201


@bp.get('/addresses')
def get_address():
    try:
        address_id = request.args.get('address_id', default=None)
        
        if not address_id:
            return jsonify({'error': 'Request must contain query parameter: address_id'}), 400
        
        address = address_repository.get_address(address_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'address': AddressDTO(address).map_address_dto_to_json()}), 200


@bp.delete('/addresses')
def delete_address():
    try:
        address_id = request.args.get('address_id', default=None)
        
        if not address_id:
            return jsonify({'error': 'Request must contain query parameter: address ID'}), 400
        
        address_repository.delete_address(address_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return '', 204
