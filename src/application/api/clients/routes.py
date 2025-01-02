from datetime import date

from flask import jsonify, request

from application.mappers import ClientDTO
from application.models import Client
from application.schemas import ClientSchema
from application.queries.orm.client import ClientORM
from . import bp


@bp.post('/add_client')
def add_client():
    if not request.is_json: 
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        client_schema = ClientSchema(**request_data)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        new_client = Client(
            client_name=client_schema.client_name,
            client_surname=client_schema.client_surname,
            birthday=client_schema.birthday,
            gender=client_schema.gender,
            registration_date=date.today(),
            address_id=client_schema.address_id
        )
        ClientORM.add_client(new_client)

    return jsonify({'message': 'Success'}), 200


@bp.delete('/delete_client')
def delete_client():
    if not request.is_json: 
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        client_id = int(request.json['client_id'])
        ClientORM.delete_client(client_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    
    return jsonify({'message': 'Success'}), 200


@bp.get('/get_all_clients')
def get_allclients():
    limit = request.args.get('limit', default=None)
    offset = request.args.get('offset', default=None)


@bp.get('/get_client_by_name_and_surname')
def get_client_by_name_and_surname():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        name = str(request_data['name'])
        surname = str(request_data['surname'])
        client = ClientORM.get_client_by_name_and_surname(name, surname)
        return jsonify({'message': 'Success', 'client': ClientDTO(client).map_client_dto_to_json()}), 200
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    

@bp.post('/change_client_address')
def change_client_address():
    pass
