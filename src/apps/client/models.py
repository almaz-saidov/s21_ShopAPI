import uuid
from datetime import date, datetime, timezone
from enum import Enum as PyEnum
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.address.models import Address
from settings.database import Base


class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"

    def __str__(self):
        return self.name


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_surname: Mapped[str] = mapped_column(String(255), nullable=False)
    birthday: Mapped[Optional[date]] = mapped_column(Date(), nullable=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=timezone.utc)
    )

    address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"), nullable=True
    )
    address: Mapped["Address"] = relationship("Address", lazy="joined")
