from sqlalchemy import update

from application.database import get_db_session
from application.models import Product


class ProductORM:
    # Добавление товара (на вход подается json, соответствующей структуре, описанной сверху).
    @staticmethod
    def add_product():
        pass

    @staticmethod
    def delete_product(prudct_id: int):
        with get_db_session() as db_session:
            product_to_delete = db_session.query(Product).filter(Product.id == prudct_id).one_or_none()
            if product_to_delete:
                db_session.delete(product_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Product with id {prudct_id} not found')

    # Получение всех доступных товаров
    @staticmethod
    def get_all_available_products():
        pass

    @staticmethod
    def get_product(product_id: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            if not product:
                raise Exception(f'Product with id {product_id} not found')                
            return product

    @staticmethod
    def reduce_product(product_id: int, n: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product:
                raise Exception(f'Product with id {product_id} not found')

            if product.available_stock < n:
                raise Exception(f'Available stock is {product.available_stock}')
            
            query = update(Product).where(Product.id == product_id).values(available_stock=Product.available_stock - n)
            db_session.execute(query)
            db_session.commit()