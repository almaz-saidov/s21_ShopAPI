from datetime import date

from sqlalchemy import (BigInteger, Column, Date,
                        ForeignKey, Integer, String)
from sqlalchemy.dialects.postgresql import UUID

from . import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    available_stock = Column(Integer, nullable=False)
    last_update_date = Column(Date, default=date.today)
    supplier_id = Column(BigInteger, ForeignKey('supplier.id'), nullable=False)
    image_id = Column(UUID, ForeignKey('image.id'))
