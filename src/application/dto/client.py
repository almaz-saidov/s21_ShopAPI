import json

from application.models import Client
from application.repositories.address import AddressRepository
from .address import AddressDTO


class ClientDTO:
    def __init__(self, client: Client):
        self.id = client.id
        self.client_name = client.client_name
        self.client_surname = client.client_surname
        self.birthday = client.birthday.isoformat()
        self.gender = client.gender
        self.registration_date = client.registration_date.isoformat()
        self.address = AddressDTO(AddressRepository.get_address(client.address_id)).map_address_dto_to_json()

    def map_client_dto_to_json(self):
        return json.dumps(self.__dict__)
