from fastapi import FastAPI

from apps.address.router import router as address_router
from apps.category.router import router as category_router
from apps.client.router import router as client_router
from apps.product.router import router as product_router
from apps.product_image.router import router as product_image_router
from apps.supplier.router import router as supplier_router

app = FastAPI(root_path="/api/v1")

app.include_router(address_router)
app.include_router(category_router)
app.include_router(client_router)
app.include_router(product_router)
app.include_router(product_image_router)
app.include_router(supplier_router)
