from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.address import AddressDTO
from application.dto.client import ClientDTO
from application.models.address import Address
from application.models.client import Client


class ClientRepository:
    def add_client(self, client_dto: ClientDTO):
        with get_db_session() as db_session:
            db_session.add(Client(
                client_name=client_dto.client_name,
                client_surname=client_dto.client_surname,
                birthday=client_dto.birthday,
                gender=client_dto.gender,
                registration_date=client_dto.registration_date,
                address_id=client_dto.address_id
            ))
            db_session.commit()

    def delete_client(self, client_id: int):
        with get_db_session() as db_session:
            client_to_delete = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            
            if not client_to_delete:
                raise NotFound(f'Client with id {client_id} not found')
            
            db_session.delete(client_to_delete)
            db_session.commit()

    def get_all_clients(self, limit: int=0, offset: int=0):
        with get_db_session() as db_session:
            clients = db_session.query(Client).limit(limit).offset(offset).all()
            return clients

    def get_client_by_name_and_surname(self, name: str, surname: str):
        with get_db_session() as db_session:
            client = db_session.query(Client).filter(Client.client_name == name, Client.client_surname == surname).one_or_none()
            
            if not client:
                raise NotFound(f'Client with name {name} and surname {surname} not found')
            
            return client

    def change_client_address(self, client_id: int, new_address: AddressDTO):
        with get_db_session() as db_session:
            client_to_change_address = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            
            if not client_to_change_address:
                raise NotFound(f'Client with id {client_id} not found')
            
            query = update(Address).where(Address.id == client_to_change_address.address_id).values(country=new_address.country, city=new_address.city, street=new_address.street)
            db_session.execute(query)
            db_session.commit()

            client = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            address = db_session.query(Address).filter(Address.id == client.address_id).one_or_none()
            return client, address
