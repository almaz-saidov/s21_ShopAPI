import uuid
from functools import lru_cache

from fastapi import HTTPException, status

from apps.address.models import Address
from apps.address.repositories import AddressRepository
from apps.address.schemas import SAddressPost, SAddressPut
from settings.services import BaseService


class AddressService(BaseService[AddressRepository]):
    async def get_address(self, id: uuid.UUID) -> Address:
        address = await self.repository.find_one(id=id)
        if address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден."
            )

        return address

    async def get_addresses(self) -> list[Address]:
        return await self.repository.find_all()

    async def add_address(self, address: SAddressPost) -> Address:
        return await self.repository.add_one(data=address.model_dump())

    async def update_address(
        self,
        id: uuid.UUID,
        addres: SAddressPut,
    ) -> Address:
        updated_address = await self.repository.update_one(
            data=addres.model_dump(),
            id=id,
        )
        if updated_address is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден."
            )

        return updated_address

    async def delete_address(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_address_service() -> AddressService:
    return AddressService(repo=AddressRepository)
