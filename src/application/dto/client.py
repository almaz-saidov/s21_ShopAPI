from datetime import date
import json

from application.repositories.address import AddressRepository

address_reposirory = AddressRepository()


class ClientDTO:
    def __init__(self, id: int | None, client_name: str, client_surname: str, birthday: date, gender: str, registration_date: date, address_id: int):
        self.id = id
        self.client_name = client_name
        self.client_surname = client_surname
        self.birthday = birthday.isoformat()
        self.gender = gender
        self.registration_date = registration_date.isoformat()
        self.address = address_reposirory.get_address(address_id).map_address_dto_to_json()

    def map_client_dto_to_json(self):
        return json.dumps(self.__dict__)
