from datetime import date
from typing import Optional

from sqlalchemy.dialects.postgresql import UUID

from pydantic import BaseModel


class AddressSchema(BaseModel):
    id: Optional[int]
    country: str
    city: str
    street: str

    class Config:
        orm_mode = True


class ClientSchema(BaseModel):
    id: Optional[int]
    client_name: str
    client_surname: str
    birthday: date
    gender: str
    registration_date: date = date.today()
    address_id: int

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    id: Optional[UUID]
    _image: bytes

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: Optional[int]
    name: str
    category: str
    price: int
    available_stock: int
    last_update_date: date
    supplier_id: int
    image_id: UUID

    class Config:
        orm_mode = True


class SupplierSchema(BaseModel):
    id: Optional[int]
    name: str
    address_id: int
    phone_number: str

    class Config:
        orm_mode = True
