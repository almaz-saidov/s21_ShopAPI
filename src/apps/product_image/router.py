import uuid

from fastapi import APIRouter, File, Response, status, UploadFile

from apps.product_image.schemas import SProductImageResponse
from apps.product_image.services import get_product_image_service

router = APIRouter(
    prefix="/image",
    tags=["Изображение"],
)


@router.get("/{id}")
async def get_image(id: uuid.UUID):
    image = await get_product_image_service().get_image(id=id)
    return Response(
        content=image.image,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={image.filename}"},
    )


@router.get("/product/{id}")
async def get_product_image(id: uuid.UUID):
    image = await get_product_image_service().get_image_by_product_id(id=id)
    return Response(
        content=image.image,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={image.filename}"},
    )


@router.post("/{id}", response_model=SProductImageResponse)
async def add_image(
    id: uuid.UUID,
    image: UploadFile = File(..., description="Изображение товара"),
):
    return await get_product_image_service().add_image(
        id=id,
        image=image,
    )


@router.put("/{id}")
async def update_image(
    id: uuid.UUID,
    image: UploadFile = File(..., description="Изображение товара"),
):
    pass


@router.delete("/{id}")
async def delete_image(id: uuid.UUID):
    await get_product_image_service().delete_image(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
