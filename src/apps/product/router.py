import uuid

from fastapi import APIRouter, Query, Response, status

from apps.product.schemas import SProductPost, SProduct
from apps.product.services import get_product_service

router = APIRouter(
    prefix="/product",
    tags=["Товар"],
)


@router.get("/list", response_model=list[SProduct])
async def get_all_available_products():
    return await get_product_service().get_all_available_products()


@router.get("/{id}", response_model=SProduct)
async def get_product(id: uuid.UUID):
    return await get_product_service().get_product(id=id)


@router.post("", response_model=SProduct)
async def add_product(product: SProductPost):
    return await get_product_service().add_product(product=product)


@router.patch("/{id}", response_model=SProduct)
async def reduce_product_count(
    id: uuid.UUID,
    amount: int = Query(1, ge=1),
):
    return await get_product_service().reduce_product_count(
        id=id,
        amount=amount,
    )


@router.delete("/{id}")
async def delete_product(id: uuid.UUID):
    await get_product_service().delete_product(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
