import json

from application.models.address import Address


class AddressDTO:
    def __init__(self, address: Address):
        self.id = address.id
        self.country = address.country
        self.city = address.city
        self.street = address.street

    def map_address_dto_to_json(self):
        return json.dumps(self.__dict__)
