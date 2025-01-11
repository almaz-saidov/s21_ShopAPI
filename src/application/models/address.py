from sqlalchemy import BigInteger, Column, String

from . import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)
