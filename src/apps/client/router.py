import uuid

from fastapi import APIRouter, Query, Response, status

from apps.address.schemas import SAddressPut
from apps.client.schemas import SClient, SClientPost
from apps.client.services import get_client_service

router = APIRouter(
    prefix="/client",
    tags=["Клиент"],
)


@router.get("/list", response_model=list[SClient])
async def get_clients(
    offset: int = Query(None, ge=0),
    limit: int = Query(None, ge=1, le=20),
):
    return await get_client_service().get_all_clients(
        offset=offset,
        limit=limit,
    )


@router.get("", response_model=SClient)
async def get_client(
    client_name: str = Query(
        ...,
        description="Имя клиента",
        example="Иван",
    ),
    client_surname: str = Query(
        ...,
        description="Фамилия клиента",
        example="Иванов",
    ),
):
    return await get_client_service().get_client(
        client_name=client_name,
        client_surname=client_surname,
    )


@router.post("", response_model=SClientPost)
async def add_client(client: SClientPost):
    return await get_client_service().add_client(client=client)


@router.patch("/{id}", response_model=SClient)
async def update_client_address(id: uuid.UUID, address: SAddressPut):
    return await get_client_service().update_client_address(
        id=id,
        address=address,
    )


@router.delete("/{id}")
async def delete_client(id: uuid.UUID):
    await get_client_service().delete_client(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
