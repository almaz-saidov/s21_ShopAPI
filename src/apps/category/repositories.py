from apps.category.models import Category
from settings.repositories import SQLAlchemyORMRepository


class CategoryRepository(SQLAlchemyORMRepository[Category]):
    cls_model = Category
