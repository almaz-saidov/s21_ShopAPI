import json

from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.address import AddressDTO
from application.dto.client import ClientDTO
from application.models import Address, Client


class ClientRepository:
    def add_client(self, client_dto: ClientDTO):
        with get_db_session() as db_session:
            new_client = Client(
                client_name=client_dto.client_name,
                client_surname=client_dto.client_surname,
                birthday=client_dto.birthday,
                gender=client_dto.gender,
                registration_date=client_dto.registration_date,
                address_id=json.loads(client_dto.address).get('id')
            )
            db_session.add(new_client)
            db_session.commit()
            return ClientDTO(
                new_client.id,
                new_client.client_name,
                new_client.client_surname,
                new_client.birthday,
                new_client.gender,
                new_client.registration_date,
                new_client.address_id
            )

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
            return [
                ClientDTO(
                    client.id,
                    client.client_name,
                    client.client_surname,
                    client.birthday,
                    client.gender,
                    client.registration_date,
                    client.address_id
                ).map_client_dto_to_json()
                for client in clients
            ]

    def get_client_by_name_and_surname(self, name: str, surname: str):
        with get_db_session() as db_session:
            client = db_session.query(Client).filter(Client.client_name == name, Client.client_surname == surname).one_or_none()
            
            if not client:
                raise NotFound(f'Client with name {name} and surname {surname} not found')
            
            return ClientDTO(
                client.id,
                client.client_name,
                client.client_surname,
                client.birthday,
                client.gender,
                client.registration_date,
                client.address_id
            )

    def change_client_address(self, client_id: int, new_address_dto: AddressDTO):
        with get_db_session() as db_session:
            client_to_change_address = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            
            if not client_to_change_address:
                raise NotFound(f'Client with id {client_id} not found')
            
            query = update(Address).where(Address.id == client_to_change_address.address_id).values(country=new_address_dto.country, city=new_address_dto.city, street=new_address_dto.street)
            db_session.execute(query)
            db_session.commit()

            client = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            return ClientDTO(
                client.id,
                client.client_name,
                client.client_surname,
                client.birthday,
                client.gender,
                client.registration_date,
                client.address_id
            )
