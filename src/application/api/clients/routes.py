from datetime import date

from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.dto.address import AddressDTO
from application.dto.client import ClientDTO
from application.repositories.client import ClientRepository
from application.schemas import AddressSchema, ClientSchema
from . import bp

client_repository = ClientRepository()


@bp.post('/clients')
def add_client():
    if not request.is_json: 
        return jsonify({'error': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        client_schema = ClientSchema(**request_data)
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        new_client_dto = ClientDTO(
            id=None,
            client_name=client_schema.client_name,
            client_surname=client_schema.client_surname,
            birthday=client_schema.birthday,
            gender=client_schema.gender,
            registration_date=date.today(),
            address_id=client_schema.address_id
        )
        added_client_dto = client_repository.add_client(new_client_dto)
        return jsonify({'new client': added_client_dto.map_client_dto_to_json()}), 201


@bp.delete('/clients')
def delete_client():
    try:
        client_id = request.args.get('client_id', default=None)
        
        if not client_id:
            return jsonify({'error': 'Request must contain query parameter: client_id'}), 400
        
        client_repository.delete_client(client_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return '', 204


@bp.get('/all-clients')
def get_all_clients():
    try:
        limit = request.args.get('limit', default=None)
        offset = request.args.get('offset', default=None)
        clients_dto = client_repository.get_all_clients(limit, offset)
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'all clients': clients_dto}), 200


@bp.get('/clients')
def get_client_by_name_and_surname():
    try:
        name = request.args.get('name', default=None)
        surname = request.args.get('surname', default=None)
        
        if not name or not surname: 
            return jsonify({'error': 'Request must contain query parameters: name, surname'}), 400
        
        client_dto = client_repository.get_client_by_name_and_surname(name, surname)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'client': client_dto.map_client_dto_to_json()}), 200


@bp.patch('/clients')
def change_client_address():
    if not request.is_json:
        return jsonify({'error': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        client_id = request.args.get('client_id', default=None)
        
        if not client_id: 
            return jsonify({'error': 'Request must contain query parameter: client_id'}), 400
        
        new_address_schema = AddressSchema(**request_data)
        new_address_dto = AddressDTO(
            id=None,
            country=new_address_schema.country,
            city=new_address_schema.city,
            street=new_address_schema.street
        )
        client_dto = client_repository.change_client_address(client_id, new_address_dto)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'client': client_dto.map_client_dto_to_json()}), 200
