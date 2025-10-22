from typing import Optional
import uuid
from datetime import date, datetime

from pydantic import BaseModel

from apps.address.schemas import SAddress
from apps.client.models import Gender


class SClientPost(BaseModel):
    client_name: str
    client_surname: str
    birthday: date
    gender: Gender


class SClient(SClientPost):
    id: uuid.UUID
    registration_date: datetime
    address: Optional[SAddress]
