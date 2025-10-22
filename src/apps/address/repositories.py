from apps.address.models import Address
from settings.repositories import SQLAlchemyORMRepository


class AddressRepository(SQLAlchemyORMRepository[Address]):
    cls_model = Address
