from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.models.address import Address


class AddressRepository:
    def add_address(self, address: Address):
        with get_db_session() as db_session:
            db_session.add(address)
            db_session.commit()

    def get_address(self, address_id: int):
        with get_db_session() as db_session:
            address = db_session.query(Address).filter(Address.id == address_id).one_or_none()
            
            if not address:
                raise NotFound(f'Address with id {address_id} not found')                
            
            return address

    def delete_address(self, address_id: int):
        with get_db_session() as db_session:
            address_to_delete = db_session.query(Address).filter(Address.id == address_id).one_or_none()
            
            if not address_to_delete:
                raise NotFound(f'Address with id {address_id} not found')
            
            db_session.delete(address_to_delete)
            db_session.commit()
