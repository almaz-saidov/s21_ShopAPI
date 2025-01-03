import json

from sqlalchemy import update

from application.database import get_db_session
from application.models import Address, Supplier


class SupplierORM:
    @staticmethod
    def add_supplier(new_supplier: Supplier):
        with get_db_session() as db_session:
            db_session.add(new_supplier)
            db_session.commit()

    @staticmethod
    def delete_supplier(supplier_id: int):
        with get_db_session() as db_session:
            supplier_to_delete = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            if supplier_to_delete:
                db_session.delete(supplier_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Client with id {supplier_id} not found')

    @staticmethod
    def get_all_suppliers():
        with get_db_session() as db_session:
            return db_session.query(Supplier).all()

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        with get_db_session() as db_session:
            supplier = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            if not supplier:
                raise Exception(f'Supplier with id {supplier_id} not found')
            return supplier

    @staticmethod
    def change_supplier_address(supplier_id: int, new_address: Address):
        with get_db_session() as db_session:
            supplier_to_change_address = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            
            if not supplier_to_change_address:
                raise Exception(f'Client with id {supplier_id} not found')
            
            new_address = json.loads(new_address)
            query = update(Address).where(Address.id == supplier_to_change_address.address_id).values(country=new_address['country'], city=new_address['city'], street=new_address['street'])
            db_session.execute(query)
            db_session.commit()
