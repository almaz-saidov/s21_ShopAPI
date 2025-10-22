import uuid
from functools import lru_cache

from fastapi import HTTPException, status

from apps.address.schemas import SAddress, SAddressPut
from apps.supplier.models import Supplier
from apps.supplier.repositories import SupplierRepository
from apps.supplier.schemas import SSupplier, SSupplierPost
from settings.services import BaseService


class SupplierService(BaseService[SupplierRepository]):
    async def get_all_suppliers(self) -> list[Supplier]:
        return await self.repository.find_suppliers()

    async def get_supplier(
        self,
        id: uuid.UUID,
    ) -> Supplier:
        supplier = await self.repository.find_supplier(id=id)
        if supplier is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поставщик не найден.",
            )

        return supplier

    async def add_supplier(self, supplier: SSupplierPost) -> Supplier:
        return await self.repository.add_one(data=supplier.model_dump())

    async def update_supplier_address(
        self,
        id: uuid.UUID,
        address: SAddressPut,
    ) -> SSupplier:
        supplier = await self.repository.update_supplier_address(
            id=id,
            data=address.model_dump(),
        )
        address = SAddress(
            id=supplier.address.id,
            country=supplier.address.country,
            city=supplier.address.city,
            street=supplier.address.street,
        )

        return SSupplier(
            id=supplier.id,
            name=supplier.name,
            phone_number=supplier.phone_number,
            address=address,
        )

    async def delete_supplier(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_supplier_service() -> SupplierService:
    return SupplierService(repo=SupplierRepository)
