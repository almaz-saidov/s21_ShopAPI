from datetime import date
from uuid import uuid4

from sqlalchemy import (BigInteger, Column, Date,
                        ForeignKey, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import LargeBinary

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)


class Client(Base):
    __tablename__ = 'client'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)
    client_surname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    registration_date = Column(Date, default=date.today)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)


class Image(Base):
    __tablename__ = 'image'

    id = Column(UUID, primary_key=True, default=uuid4)
    data = Column(LargeBinary)


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


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)
    phone_number = Column(String(16), nullable=False)
