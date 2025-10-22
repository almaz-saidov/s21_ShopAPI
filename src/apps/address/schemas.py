import uuid

from pydantic import BaseModel


class SAddressPost(BaseModel):
    country: str
    city: str
    street: str


class SAddressPut(SAddressPost): ...


class SAddress(SAddressPost):
    id: uuid.UUID
