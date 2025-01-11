from sqlalchemy import BigInteger, Column, ForeignKey, String

from . import Base


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)
    phone_number = Column(String(16), nullable=False)
