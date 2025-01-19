from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.product import ProductDTO
from application.models import Product


class ProductRepository:
    def add_product(self, product_dto: ProductDTO):
        with get_db_session() as db_session:
            new_product = Product(
                name=product_dto.name,
                category=product_dto.category,
                price=product_dto.price,
                available_stock=product_dto.available_stock,
                last_update_date=product_dto.last_update_date,
                supplier_id=product_dto.supplier_id,
                image_id=product_dto.image_id
            )
            db_session.add(new_product)
            db_session.commit()

            return ProductDTO(
                id=new_product.id,
                name=new_product.name,
                category=new_product.category,
                price=new_product.price,
                available_stock=new_product.available_stock,
                last_update_date=new_product.last_update_date,
                supplier_id=new_product.supplier_id,
                image_id=new_product.image_id
            )

    def delete_product(self, product_id: int):
        with get_db_session() as db_session:
            product_to_delete = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product_to_delete:
                raise NotFound(f'Product with id {product_id} not found')
            
            db_session.delete(product_to_delete)
            db_session.commit()

    def get_all_available_products(self):
        with get_db_session() as db_session:
            all_available_products = db_session.query(Product).filter(Product.available_stock > 0).all()
            return [
                ProductDTO(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    price=product.price,
                    available_stock=product.available_stock,
                    last_update_date=product.last_update_date,
                    supplier_id=product.supplier_id,
                    image_id=product.image_id
                ).map_product_dto_to_json()
                for product in all_available_products
            ]

    def get_product_by_id(self, product_id: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product:
                raise NotFound(f'Product with id {product_id} not found')                
            
            return ProductDTO(
                id=product.id,
                name=product.name,
                category=product.category,
                price=product.price,
                available_stock=product.available_stock,
                last_update_date=product.last_update_date,
                supplier_id=product.supplier_id,
                image_id=product.image_id
            )

    def reduce_product(self, product_id: int, reduce_by: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product:
                raise NotFound(f'Product with id {product_id} not found')

            if product.available_stock < reduce_by:
                raise Exception(f'Available stock is {product.available_stock}')
            
            query = update(Product).where(Product.id == product_id).values(available_stock=Product.available_stock - reduce_by)
            db_session.execute(query)
            db_session.commit()
            
            return ProductDTO(
                id=product.id,
                name=product.name,
                category=product.category,
                price=product.price,
                available_stock=product.available_stock,
                last_update_date=product.last_update_date,
                supplier_id=product.supplier_id,
                image_id=product.image_id
            )
