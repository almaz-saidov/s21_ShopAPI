import uuid
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.address.models import Address
from settings.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id", ondelete="CASCADE"), nullable=True
    )
    address: Mapped["Address"] = relationship("Address", lazy="joined")
