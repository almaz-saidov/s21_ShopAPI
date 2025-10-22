import uuid

from fastapi import APIRouter, Response, status

from apps.address.schemas import SAddress, SAddressPost, SAddressPut
from apps.address.services import get_address_service

router = APIRouter(
    prefix="/address",
    tags=["Адрес"],
)


@router.get("/list", response_model=list[SAddress])
async def get_addresses():
    return await get_address_service().get_addresses()


@router.get("/{id}", response_model=SAddress)
async def get_address(id: uuid.UUID):
    return await get_address_service().get_address(id=id)


@router.post("", response_model=SAddress)
async def add_address(address: SAddressPost):
    return await get_address_service().add_address(address=address)


@router.put("/{id}", response_model=SAddress)
async def update_address(id: uuid.UUID, address: SAddressPut):
    return await get_address_service().update_address(
        id=id,
        addres=address,
    )


@router.delete("/{id}")
async def delete_address(id: uuid.UUID):
    await get_address_service().delete_address(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
