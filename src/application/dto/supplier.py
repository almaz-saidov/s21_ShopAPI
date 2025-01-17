import json

from application.repositories.address import AddressRepository

address_repository = AddressRepository()


class SupplierDTO:
    def __init__(self, id: int | None, name: str, address_id: int, phone_number: str):
        self.id = id
        self.name = name
        self.address = address_repository.get_address(address_id).map_address_dto_to_json()
        self.phone_number = phone_number

    def map_supplier_dto_to_json(self):
        return json.dumps(self.__dict__)
