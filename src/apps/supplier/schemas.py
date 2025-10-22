from typing import Optional
import uuid

from pydantic import BaseModel

from apps.address.schemas import SAddress


class SSupplierPost(BaseModel):
    name: str
    phone_number: str


class SSupplier(SSupplierPost):
    id: uuid.UUID
    address: Optional[SAddress]
