import json

from application.models import Supplier
from application.repositories.address import AddressRepository
from .address import AddressDTO


class SupplierDTO:
    def __init__(self, supplier: Supplier):
        self.id = supplier.id
        self.name = supplier.name
        self.address = AddressDTO(AddressRepository.get_address(supplier.address_id)).map_address_dto_to_json()
        self.phone_number = supplier.phone_number

    def map_supplier_dto_to_json(self):
        return json.dumps(self.__dict__)
