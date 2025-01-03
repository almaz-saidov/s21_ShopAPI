from flask import jsonify, request

from application.mappers import AddressDTO, SupplierDTO
from application.models import Address, Supplier
from application.schemas import AddressSchema, SupplierSchema
from application.queries.orm.supplier import SupplierORM
from . import bp


@bp.post('/add_supplier')
def add_supplier():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        supplier_schema = SupplierSchema(**request_data)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        new_supplier = Supplier(
            name=supplier_schema.name,
            address_id=supplier_schema.address_id,
            phone_number=supplier_schema.phone_number
        )
        SupplierORM.add_supplier(new_supplier)
        return jsonify({'message': 'Success'}), 200


@bp.delete('/delete_supplier')
def delete_supplier():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        supplier_id = int(request.json['supplier_id'])
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        SupplierORM.delete_supplier(supplier_id)
        return jsonify({'message': 'Success'})
    

@bp.get('/get_all_suppliers')
def get_all_suppliers():
    try:
        all_suppliers = SupplierORM.get_all_suppliers()
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        json_all_suppliers = [SupplierDTO(supplier).map_supplier_dto_to_json() for supplier in all_suppliers]
        return jsonify({'message': 'Success', 'all_suppliers': json_all_suppliers}), 200


@bp.get('/get_supplier_by_id')
def get_supplier_by_id():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        supplier_id = int(request.json['supplier_id'])
        supplier = SupplierORM.get_supplier_by_id(supplier_id)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success', 'supplier': SupplierDTO(supplier).map_supplier_dto_to_json()})


@bp.post('/change_supplier_address')
def change_supplier_address():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        supplier_id = int(request_data['supplier_id'])
        new_address_schema = AddressSchema(**request_data['new_address'])
        new_address = Address(
            country=new_address_schema.country,
            city=new_address_schema.city,
            street=new_address_schema.street
        )
        SupplierORM.change_supplier_address(supplier_id, AddressDTO(new_address).map_address_dto_to_json())
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'message': 'Success'}), 200
