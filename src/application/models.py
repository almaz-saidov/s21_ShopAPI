from datetime import date
from uuid import uuid4

from sqlalchemy import (BigInteger, Column, Date,
                        ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import LargeBinary

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    country = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)

    # clients = relationship('Client', back_populates='address')
    # suppliers = relationship('Supplier', back_populates='address')


class Client(Base):
    __tablename__ = 'client'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)
    client_surname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    registration_date = Column(Date, default=date.today)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)

    # address = relationship("Address", back_populates="clients")


class Image(Base):
    __tablename__ = 'image'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    _image = Column(LargeBinary)


class Product(Base):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    available_stock = Column(Integer, nullable=False)
    last_update_date = Column(Date, default=date.today)
    supplier_id = Column(BigInteger, ForeignKey('supplier.id'), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey('image.id'), nullable=False)

    # supplier = relationship('Supplier', uselist=False, back_populates='supplier')
    # image = relationship('Image', backref='product')


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)
    phone_number = Column(String(16), nullable=False)

    # address = relationship('Address', back_populates='suppliers')
