import json

from sqlalchemy import update

from application.database import get_db_session
from application.models import Address, Client


class ClientORM:
    @staticmethod
    def add_client(client: Client):
        with get_db_session() as db_session:
            db_session.add(client)
            db_session.commit()

    @staticmethod
    def delete_client(client_id: int):
        with get_db_session() as db_session:
            client_to_delete = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            if not client_to_delete:
                raise Exception(f'Client with id {client_id} not found')
            
            db_session.delete(client_to_delete)
            db_session.commit()

    @staticmethod
    def get_all_clients(limit: int=0, offset: int=0):
        with get_db_session() as db_session:
            clients = db_session.query(Client).limit(limit).offset(offset).all()
            return clients

    @staticmethod
    def get_client_by_name_and_surname(name: str, surname: str):
        with get_db_session() as db_session:
            client = db_session.query(Client).filter(Client.client_name == name, Client.client_surname == surname).one_or_none()
            if not client:
                raise Exception(f'Client with name {name} and surname {surname} not found')
            
            return client

    @staticmethod
    def change_client_address(client_id: int, new_address: json.dumps):
        with get_db_session() as db_session:
            client_to_change_address = db_session.query(Client).filter(Client.id == client_id).one_or_none()
            if not client_to_change_address:
                raise Exception(f'Client with id {client_id} not found')
            
            new_address = json.loads(new_address)
            query = update(Address).where(Address.id == client_to_change_address.address_id).values(country=new_address['country'], city=new_address['city'], street=new_address['street'])
            db_session.execute(query)
            db_session.commit()
