import uuid
from functools import lru_cache

from fastapi import HTTPException, status

from apps.product.models import Product
from apps.product.repositories import ProductRepository
from apps.product.schemas import SProductPost
from apps.supplier.services import get_supplier_service
from settings.services import BaseService


class ProductService(BaseService[ProductRepository]):
    async def get_product(self, id: uuid.UUID) -> Product:
        product = await self.repository.find_one(id=id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден.",
            )

        return product

    async def get_all_available_products(self) -> list[Product]:
        return await self.repository.find_all_available_products()

    async def add_product(
        self,
        product: SProductPost,
    ) -> Product:
        supplier = await get_supplier_service().get_supplier(id=product.supplier_id)
        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поставщик не найден.",
            )

        return await self.repository.add_one(data=product.model_dump())

    async def reduce_product_count(
        self,
        id: uuid.UUID,
        amount: int,
    ) -> Product:
        return await self.repository.reduce_product_amount(
            id=id,
            amount=amount,
        )

    async def delete_product(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_product_service() -> ProductService:
    return ProductService(repo=ProductRepository)
