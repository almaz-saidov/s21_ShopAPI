import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.category.models import Category
from apps.product_image.models import ProductImage
from apps.supplier.models import Supplier
from settings.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    available_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_update_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(tz=timezone.utc)
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=True
    )
    category: Mapped["Category"] = relationship("Category", lazy="select")

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE"), nullable=False
    )
    supplier: Mapped["Supplier"] = relationship("Supplier", lazy="select")

    image_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("product_images.id", ondelete="CASCADE"), nullable=True
    )
    image: Mapped["ProductImage"] = relationship("ProductImage", lazy="select")
