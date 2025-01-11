from datetime import date

from sqlalchemy import (BigInteger, Column, Date,
                        ForeignKey, String)

from . import Base


class Client(Base):
    __tablename__ = 'client'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    client_name = Column(String(255), nullable=False)
    client_surname = Column(String(255), nullable=False)
    birthday = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    registration_date = Column(Date, default=date.today)
    address_id = Column(BigInteger, ForeignKey('address.id'), nullable=False)
