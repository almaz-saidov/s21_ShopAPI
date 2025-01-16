from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.address import AddressDTO
from application.models import Address


class AddressRepository:
    def add_address(self, address_dto: AddressDTO):
        with get_db_session() as db_session:
            new_address = Address(
                country=address_dto.country,
                city = address_dto.city,
                street=address_dto.street
            )
            db_session.add(new_address)
            db_session.commit()
            return AddressDTO(new_address)

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
