from fastapi import APIRouter, FastAPI

from apps.address.router import router as address_router
from apps.category.router import router as category_router
from apps.client.router import router as client_router
from apps.product.router import router as product_router
from apps.product_image.router import router as product_image_router
from apps.supplier.router import router as supplier_router

app = FastAPI()

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(address_router)
api_router.include_router(category_router)
api_router.include_router(client_router)
api_router.include_router(product_router)
api_router.include_router(product_image_router)
api_router.include_router(supplier_router)

app.include_router(api_router)
