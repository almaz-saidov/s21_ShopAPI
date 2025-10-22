from typing import Optional
import uuid

from pydantic import BaseModel


class SProductPost(BaseModel):
    name: str
    price: int
    available_stock: int
    supplier_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    image_id: Optional[uuid.UUID]


class SProduct(SProductPost):
    id: uuid.UUID
