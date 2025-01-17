from flask import jsonify, request
from werkzeug.exceptions import NotFound

from application.dto.address import AddressDTO
from application.dto.supplier import SupplierDTO
from application.schemas import AddressSchema, SupplierSchema
from application.repositories.supplier import SupplierRepository
from . import bp

supplier_repository = SupplierRepository()


@bp.post('/suppliers')
def add_supplier():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        supplier_schema = SupplierSchema(**request_data)
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        new_supplier_dto = SupplierDTO(
            id=None,
            name=supplier_schema.name,
            address_id=supplier_schema.address_id,
            phone_number=supplier_schema.phone_number
        )
        added_supplier_dto = supplier_repository.add_supplier(new_supplier_dto)
        return jsonify({'new supplier': added_supplier_dto.map_supplier_dto_to_json()}), 201


@bp.delete('/suppliers')
def delete_supplier():
    try:
        supplier_id = int(request.args.get('supplier_id', default=None))
        
        if not supplier_id:
            return jsonify({'message': 'Request must contain query parameter: supplier_id'}), 400
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        supplier_repository.delete_supplier(supplier_id)
        return '', 204
    

@bp.get('/all-suppliers')
def get_all_suppliers():
    try:
        suppliers_dto = supplier_repository.get_all_suppliers()
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'all suppliers': suppliers_dto}), 200


@bp.get('/suppliers')
def get_supplier_by_id():
    try:
        supplier_id = int(request.args.get('supplier_id', default=None))
        
        if not supplier_id:
            return jsonify({'error': 'Request must contain query parameter: supplier_id'}), 400
        
        supplier_dto = supplier_repository.get_supplier_by_id(supplier_id)
    except NotFound as e:
        return jsonify({'error': f'{e}'}), 404
    except Exception as e:
        return jsonify({'error': f'{e}'}), 400
    else:
        return jsonify({'supplier': supplier_dto.map_supplier_dto_to_json()}), 200


@bp.patch('/suppliers')
def change_supplier_address():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    try:
        request_data = request.json
        supplier_id = int(request.args.get('supplier_id', default=None))
        
        if not supplier_id:
            return jsonify({'message': 'Request must contain query parameter: supplier_id'}), 400
        
        new_address_schema = AddressSchema(**request_data)
        new_address_dto = AddressDTO(
            id=None,
            country=new_address_schema.country,
            city=new_address_schema.city,
            street=new_address_schema.street
        )
        
        supplier_dto = supplier_repository.change_supplier_address(supplier_id, new_address_dto)
    except NotFound as e:
        return jsonify({'message': f'{e}'}), 404
    except Exception as e:
        return jsonify({'message': f'{e}'}), 400
    else:
        return jsonify({'supplier': supplier_dto.map_supplier_dto_to_json()}), 200
