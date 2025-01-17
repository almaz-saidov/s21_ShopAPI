import json


class AddressDTO:
    def __init__(self, id: int | None, country: str, city: str, street: str):
        self.id = id
        self.country = country
        self.city = city
        self.street = street

    def map_address_dto_to_json(self):
        return json.dumps(self.__dict__)
