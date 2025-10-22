import uuid
from functools import lru_cache

from fastapi import HTTPException, status, UploadFile

from apps.product_image.schemas import SProductImageResponse
from apps.product.services import get_product_service
from apps.product_image.models import ProductImage
from apps.product_image.repositories import ProductImageRepository
from settings.services import BaseService


class ProductImageService(BaseService[ProductImageRepository]):
    async def get_image(self, id: uuid.UUID) -> ProductImage:
        product_image = await self.repository.find_one(id=id)
        if product_image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Изображение не найдено.",
            )

        return product_image

    async def get_image_by_product_id(self, id: uuid.UUID) -> ProductImage:
        product = await get_product_service().get_product(id=id)
        return await self.get_image(id=product.image_id)

    async def add_image(
        self,
        id: uuid.UUID,
        image: UploadFile,
    ) -> ProductImage:
        image_data = await image.read()
        added_image = await self.repository.add_image(
            id=id,
            data={
                "filename": image.filename,
                "image": image_data,
            },
        )

        return SProductImageResponse(
            id=added_image.id,
            filename=added_image.filename,
        )

    async def delete_image(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_product_image_service() -> ProductImageService:
    return ProductImageService(repo=ProductImageRepository)
