from datetime import date
from typing import Optional
import uuid

from pydantic import BaseModel, Field, SkipValidation


class AddressSchema(BaseModel):
    id: Optional[int] = None
    country: str
    city: str
    street: str

    class Config:
        from_attributes = True


class ClientSchema(BaseModel):
    id: Optional[int] = None
    client_name: str
    client_surname: str
    birthday: date = Field(SkipValidation())
    gender: str
    address_id: int

    class Config:
        from_attributes = True


class ImageSchema(BaseModel):
    id: Optional[uuid.UUID] = None
    data: bytes

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: int
    available_stock: int
    supplier_id: int
    image_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SupplierSchema(BaseModel):
    id: Optional[int] = None
    name: str
    address_id: int
    phone_number: str

    class Config:
        from_attributes = True
