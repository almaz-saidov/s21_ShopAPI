import uuid

from pydantic import BaseModel


class SProductImageResponse(BaseModel):
    id: uuid.UUID
    filename: str


class SProductImage(SProductImageResponse):
    image: bytes
