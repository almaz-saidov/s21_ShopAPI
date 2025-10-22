import uuid
from functools import lru_cache

from fastapi import HTTPException, status

from apps.category.models import Category
from apps.category.repositories import CategoryRepository
from apps.category.schemas import SCategoryPost, SCategoryPut
from settings.services import BaseService


class CategoryService(BaseService[CategoryRepository]):
    async def get_categories(self) -> list[Category]:
        return await self.repository.find_all()

    async def get_category(self, id: uuid.UUID) -> Category:
        category = await self.repository.find_one(id=id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена."
            )

        return category

    async def add_category(self, category: SCategoryPost) -> Category:
        return await self.repository.add_one(data=category.model_dump())

    async def update_category(
        self,
        id: uuid.UUID,
        category: SCategoryPut,
    ) -> Category:
        category_exists = await self.get_category(id=id)
        if category_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена."
            )

        return await self.repository.update_one(
            data=category.model_dump(),
            id=id,
        )

    async def delete_category(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_category_service() -> CategoryService:
    return CategoryService(repo=CategoryRepository)
