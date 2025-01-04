from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, SkipValidation
from sqlalchemy.dialects.postgresql import UUID


class AddressSchema(BaseModel):
    id: Optional[int] = None
    country: str
    city: str
    street: str

    class Config:
        orm_mode = True


class ClientSchema(BaseModel):
    id: Optional[int] = None
    client_name: str
    client_surname: str
    birthday: date = Field(SkipValidation())
    gender: str
    address_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ImageSchema(BaseModel):
    id: Optional[UUID] = None
    _image: bytes

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: int
    available_stock: int
    supplier_id: int
    image_id: Optional[UUID] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SupplierSchema(BaseModel):
    id: Optional[int] = None
    name: str
    address_id: int
    phone_number: str

    class Config:
        orm_mode = True
