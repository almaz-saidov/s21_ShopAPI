import uuid

from fastapi import APIRouter, Response, status

from apps.category.schemas import SCategory, SCategoryPost, SCategoryPut
from apps.category.services import get_category_service

router = APIRouter(
    prefix="/category",
    tags=["Категория"],
)


@router.get("/list", response_model=list[SCategory])
async def get_categories():
    return await get_category_service().get_categories()


@router.get("/{id}", response_model=SCategory)
async def get_category(id: uuid.UUID):
    return await get_category_service().get_category(id=id)


@router.post("", response_model=SCategory)
async def add_category(category: SCategoryPost):
    return await get_category_service().add_category(category=category)


@router.patch("/{id}", response_model=SCategory)
async def update_category(
    id: uuid.UUID,
    category: SCategoryPut,
):
    return await get_category_service().update_category(
        id=id,
        category=category,
    )


@router.delete("/{id}")
async def delete_category(id: uuid.UUID):
    await get_category_service().delete_category(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
