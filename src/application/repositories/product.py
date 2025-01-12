from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.product import ProductDTO
from application.models.product import Product


class ProductRepository:
    def add_product(self, product_dto: ProductDTO):
        with get_db_session() as db_session:
            db_session.add(Product(
                name=product_dto.name,
                category=product_dto.category,
                price=product_dto.price,
                available_stock=product_dto.available_stock,
                last_update_date=product_dto.last_update_date,
                supplier_id=product_dto.supplier_id,
                image_id=product_dto.image_id
            ))
            db_session.commit()

    def delete_product(self, product_id: int):
        with get_db_session() as db_session:
            product_to_delete = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product_to_delete:
                raise NotFound(f'Product with id {product_id} not found')
            
            db_session.delete(product_to_delete)
            db_session.commit()

    def get_all_available_products(self):
        with get_db_session() as db_session:
            return db_session.query(Product).filter(Product.available_stock > 0).all()

    def get_product_by_id(self, product_id: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product:
                raise NotFound(f'Product with id {product_id} not found')                
            
            return product

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
            
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            return product