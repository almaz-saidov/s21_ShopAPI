from application.database import get_db_session
from application.models import Address


class AddressORM:
    @staticmethod
    def add_address(address: Address):
        with get_db_session() as db_session:
            db_session.add(address)
            db_session.commit()

    @staticmethod
    def get_address(address_id: int):
        with get_db_session() as db_session:
            address = db_session.query(Address).filter(Address.id == address_id).one_or_none()
            if not address:
                raise Exception(f'Address with id {address_id} not found')
            return address

    @staticmethod
    def delete_address(address_id: int):
        with get_db_session() as db_session:
            address_to_delete = db_session.query(Address).filter(Address.id == address_id).one_or_none()
            if address_to_delete:
                db_session.delete(address_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Address with id {address_id} not found')
