import uuid

from fastapi import APIRouter, Response, status

from apps.address.schemas import SAddressPut
from apps.supplier.schemas import SSupplier, SSupplierPost
from apps.supplier.services import get_supplier_service

router = APIRouter(
    prefix="/supplier",
    tags=["Поставщик"],
)


@router.get("/list", response_model=list[SSupplier])
async def get_suppliers():
    return await get_supplier_service().get_all_suppliers()


@router.get("/{id}", response_model=SSupplier)
async def get_supplier(id: uuid.UUID):
    return await get_supplier_service().get_supplier(id=id)


@router.post("", response_model=SSupplierPost)
async def add_supplier(supplier: SSupplierPost):
    return await get_supplier_service().add_supplier(supplier=supplier)


@router.patch("/{id}", response_model=SSupplier)
async def update_supplier_address(id: uuid.UUID, address: SAddressPut):
    return await get_supplier_service().update_supplier_address(
        id=id,
        address=address,
    )


@router.delete("/{id}")
async def delete_supplier(id: uuid.UUID):
    await get_supplier_service().delete_supplier(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
