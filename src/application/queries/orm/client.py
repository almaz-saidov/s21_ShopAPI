import json

from application.database import get_db_session
from application.models import Client


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
            if client_to_delete:
                db_session.delete(client_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Client with id {client_id} not found')


    # Получение всех клиентов (В данном запросе необходимо предусмотреть опциональные параметры пагинации в строке запроса: limit и offset). В случае отсутствия эти параметров возвращать весь список.
    @staticmethod
    def get_all_clients(limit: int, offset: int):
        pass

    @staticmethod
    def get_client_by_name_and_surname(name: str, surname: str):
        with get_db_session() as db_session:
            client = db_session.query(Client).where(Client.client_name == name).where(Client.client_surname == surname).one_or_none()
            if not client:
                raise Exception(f'Client with name {name} and surname {surname} not found')
            return client

    # Изменение адреса клиента (параметры: Id и новый адрес в виде json в соответствии с выше описанным форматом)
    @staticmethod
    def change_client_address(address_id: int, new_address: json.dumps):
        pass
