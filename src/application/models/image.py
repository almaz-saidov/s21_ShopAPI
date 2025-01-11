from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import LargeBinary

from . import Base


class Image(Base):
    __tablename__ = 'image'

    id = Column(UUID, primary_key=True, default=uuid4)
    data = Column(LargeBinary)
