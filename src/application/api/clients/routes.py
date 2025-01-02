from datetime import date

from flask import jsonify, request

from application.models import Client
from application.schemas import ClientSchema
from application.queries.orm.client import ClientORM
from . import bp


@bp.post('/add_client')
def client_get():
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
