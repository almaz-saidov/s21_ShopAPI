import uuid
from functools import lru_cache
from typing import Union

from fastapi import HTTPException, status

from apps.address.schemas import SAddress, SAddressPut
from apps.client.models import Client
from apps.client.repositories import ClientRepository
from apps.client.schemas import SClient, SClientPost
from settings.services import BaseService


class ClientService(BaseService[ClientRepository]):
    async def get_all_clients(
        self,
        offset: Union[int, None],
        limit: Union[int, None],
    ) -> list[Client]:
        return await self.repository.find_clients(
            offset=offset,
            limit=limit,
        )

    async def get_client(
        self,
        client_name: str,
        client_surname: str,
    ) -> Client:
        client =  await self.repository.find_client(
            client_name=client_name,
            client_surname=client_surname,
        )
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Клиент не найден.",
            )

        return client

    async def add_client(self, client: SClientPost) -> Client:
        added_client = await self.repository.add_one(data=client.model_dump())
        return await self.repository.find_client(id=added_client.id)

    async def update_client_address(
        self,
        id: uuid.UUID,
        address: SAddressPut,
    ) -> SClient:
        client = await self.repository.update_client_address(
            id=id,
            data=address.model_dump(),
        )
        address = SAddress(
            id=client.address.id,
            country=client.address.country,
            city=client.address.city,
            street=client.address.street,
        )

        return SClient(
            id=client.id,
            client_name=client.client_name,
            client_surname=client.client_surname,
            birthday=client.birthday,
            gender=client.gender,
            registration_date=client.registration_date,
            address=address,
        )

    async def delete_client(self, id: uuid.UUID) -> None:
        await self.repository.force_delete_one(id=id)


@lru_cache
def get_client_service() -> ClientService:
    return ClientService(repo=ClientRepository)
