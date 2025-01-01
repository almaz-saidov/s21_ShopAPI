from datetime import date

from sqlalchemy.dialects.postgresql import UUID

from application.models import Address, Client, Image, Product, Supplier


class AddressDTO:
    def __init__(self, id: int, country: str, city: str, street: str):
        self.id = id
        self.country = country
        self.city = city
        self.street = street


class ClientDTO:
    def __init__(self, id: int, client_name: str, client_surname: str, birthday: date, gender: str, registration_date: date):
        self.id = id
        self.client_name = client_name
        self.client_surname = client_surname
        self.birthday = birthday
        self.gender = gender
        self.registration_date = registration_date


class ImageDTO:
    def __init__(self, id: UUID, image: bytes):
        self.id = id
        self.image = image


class ProductDTO:
    def __init__(self, id: int, name: str, category: str, price: int, available_stock: int, last_update_date: date):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.available_stock = available_stock
        self.last_update_date = last_update_date


class SupplierDTO:
    def __init__(self, id: int, name: str, phone_number: str):
        self.id = id
        self.name = name
        self.phone_number = phone_number


def map_address_to_dto(address: Address) -> AddressDTO:
    return AddressDTO(id=address.id, country=address.country, city=address.city, street=address.street)


def map_client_to_dto(client: Client) -> ClientDTO:
    return ClientDTO(id=client.id, client_name=client.client_name, client_surname=client.client_surname, birthday=client.birthday, gender=client.gender, registration_date=client.registration_date)


def map_image_to_dto(image: Image) -> ImageDTO:
    return ImageDTO(id=image.id, image=image._image)


def map_product_to_dto(product: Product) -> ProductDTO:
    return ProductDTO(id=product.id, name=product.name, price=product.price, available_stock=product.available_stock, last_update_date=product.last_update_date)


def map_supplier_to_dto(supplier: Supplier) -> SupplierDTO:
    return SupplierDTO(id=supplier.id, name=supplier.name, phone_number=supplier.phone_number)


