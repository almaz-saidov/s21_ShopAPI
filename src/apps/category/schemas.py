import uuid

from pydantic import BaseModel


class SCategoryPost(BaseModel):
    name: str


class SCategoryPut(SCategoryPost): ...


class SCategory(SCategoryPost):
    id: uuid.UUID
