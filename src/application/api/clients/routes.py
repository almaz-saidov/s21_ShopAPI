from datetime import date

from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.dto.address import AddressDTO
from application.dto.client import ClientDTO
from application.models.address import Address
from application.models.client import Client
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
        new_client = Client(
            client_name=client_schema.client_name,
            client_surname=client_schema.client_surname,
            birthday=client_schema.birthday,
            gender=client_schema.gender,
            registration_date=date.today(),
            address_id=client_schema.address_id
        )
        client_dto = ClientDTO(new_client)
        client_repository.add_client(new_client)
        return jsonify({'new client': client_dto.map_client_dto_to_json()}), 201


@bp.delete('/clients')
def delete_client():
    try:
        client_id = request.args.get('cleint_id', default=None)
        
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
        clients = client_repository.get_all_clients(limit, offset)
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'all clients': [ClientDTO(client).map_client_dto_to_json() for client in clients]}), 200


@bp.get('/clients')
def get_client_by_name_and_surname():
    try:
        name = request.args.get('name', default=None)
        surname = request.args.get('surname', default=None)
        
        if not name or not surname: 
            return jsonify({'error': 'Request must contain query parameters: name, surname'}), 400
        
        client = client_repository.get_client_by_name_and_surname(name, surname)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'client': ClientDTO(client).map_client_dto_to_json()}), 200


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
        new_address = Address(
            country=new_address_schema.country,
            city=new_address_schema.city,
            street=new_address_schema.street
        )
        addres, client = client_repository.change_client_address(client_id, AddressDTO(new_address))
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'client': ClientDTO(client).map_client_dto_to_json(),
                        'address': AddressDTO(addres).map_address_dto_to_json()}), 200
