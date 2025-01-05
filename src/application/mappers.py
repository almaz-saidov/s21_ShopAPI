import json

from application.models import Address, Client, Product, Supplier
from application.queries.orm.address import AddressORM


class AddressDTO:
    def __init__(self, address: Address):
        self.id = address.id
        self.country = address.country
        self.city = address.city
        self.street = address.street

    def map_address_dto_to_json(self):
        return json.dumps(self.__dict__, indent=4)


class ClientDTO:
    def __init__(self, client: Client):
        self.id = client.id
        self.client_name = client.client_name
        self.client_surname = client.client_surname
        self.birthday = client.birthday.isoformat()
        self.gender = client.gender
        self.registration_date = client.registration_date.isoformat()
        self.address = AddressDTO(AddressORM.get_address(client.address_id)).map_address_dto_to_json()

    def map_client_dto_to_json(self):
        return json.dumps(self.__dict__, indent=4)


class ProductDTO:
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.category = product.category
        self.price = product.price
        self.available_stock = product.available_stock
        self.last_update_date = product.last_update_date.isoformat()

    def map_product_dto_to_json(self):
        return json.dumps(self.__dict__, indent=4)


class SupplierDTO:
    def __init__(self, supplier: Supplier):
        self.id = supplier.id
        self.name = supplier.name
        self.address = AddressDTO(AddressORM.get_address(supplier.address_id)).map_address_dto_to_json()
        self.phone_number = supplier.phone_number

    def map_supplier_dto_to_json(self):
        return json.dumps(self.__dict__, indent=4)
