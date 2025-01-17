import json

from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.address import AddressDTO
from application.dto.supplier import SupplierDTO
from application.models import Address, Supplier


class SupplierRepository:
    def add_supplier(self, supplier_dto: SupplierDTO):
        with get_db_session() as db_session:
            new_supplier = Supplier(
                name=supplier_dto.name,
                address_id=json.loads(supplier_dto.address).get('id'),
                phone_number=supplier_dto.phone_number
            )
            db_session.add(new_supplier)
            db_session.commit()

            return SupplierDTO(
                new_supplier.id,
                new_supplier.name,
                new_supplier.address_id,
                new_supplier.phone_number
            )

    def delete_supplier(self, supplier_id: int):
        with get_db_session() as db_session:
            supplier_to_delete = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier_to_delete:
                raise NotFound(f'Client with id {supplier_id} not found')
            
            db_session.delete(supplier_to_delete)
            db_session.commit()

    def get_all_suppliers(self):
        with get_db_session() as db_session:
            suppliers = db_session.query(Supplier).all()
            return [
                SupplierDTO(
                    supplier.id,
                    supplier.name,
                    supplier.address_id,
                    supplier.phone_number
                ).map_supplier_dto_to_json()
                for supplier in suppliers
            ]

    def get_supplier_by_id(self, supplier_id: int):
        with get_db_session() as db_session:
            supplier = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier:
                raise NotFound(f'Supplier with id {supplier_id} not found')
            
            return SupplierDTO(
                supplier.id,
                supplier.name,
                supplier.address_id,
                supplier.phone_number
            )

    def change_supplier_address(self, supplier_id: int, new_address_dto: AddressDTO):
        with get_db_session() as db_session:
            supplier_to_change_address = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier_to_change_address:
                raise NotFound(f'Client with id {supplier_id} not found')
            
            query = update(Address).where(Address.id == supplier_to_change_address.address_id).values(country=new_address_dto.country, city=new_address_dto.city, street=new_address_dto.street)
            db_session.execute(query)
            db_session.commit()

            supplier = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            return SupplierDTO(
                supplier.id,
                supplier.name,
                supplier.address_id,
                supplier.phone_number
            )
