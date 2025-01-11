import json

from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.models.address import Address
from application.models.supplier import Supplier


class SupplierORM:
    def add_supplier(self, new_supplier: Supplier):
        with get_db_session() as db_session:
            db_session.add(new_supplier)
            db_session.commit()

    def delete_supplier(self, supplier_id: int):
        with get_db_session() as db_session:
            supplier_to_delete = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier_to_delete:
                raise NotFound(f'Client with id {supplier_id} not found')
            
            db_session.delete(supplier_to_delete)
            db_session.commit()

    def get_all_suppliers(self):
        with get_db_session() as db_session:
            return db_session.query(Supplier).all()

    def get_supplier_by_id(self, supplier_id: int):
        with get_db_session() as db_session:
            supplier = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier:
                raise NotFound(f'Supplier with id {supplier_id} not found')
            
            return supplier

    def change_supplier_address(self, supplier_id: int, new_address: Address):
        with get_db_session() as db_session:
            supplier_to_change_address = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier_to_change_address:
                raise NotFound(f'Client with id {supplier_id} not found')
            
            new_address = json.loads(new_address)
            query = update(Address).where(Address.id == supplier_to_change_address.address_id).values(country=new_address['country'], city=new_address['city'], street=new_address['street'])
            db_session.execute(query)
            db_session.commit()
