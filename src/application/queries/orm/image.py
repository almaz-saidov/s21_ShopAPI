from datetime import date
import uuid

from sqlalchemy import update

from application.database import get_db_session
from application.models import Image, Product


class ImageORM:
    @staticmethod
    def add_image(byte_array: bytes, product_id: int):
        with get_db_session() as db_session:
            product_to_add_image = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            if not product_to_add_image:
                raise Exception(f'Product with id {product_id} not found')
            
            image_id = uuid.uuid4()
            new_image = Image(id=image_id, data=byte_array)
            db_session.add(new_image)
            db_session.commit()

            if product_to_add_image.image_id is not None:
                raise Exception(f'Product with id {product_id} already has image')
            query = update(Product).where(Product.id == product_to_add_image.id).values(name='changed', image_id=new_image.id, last_update_date=date.today())
            db_session.execute(query)
            db_session.commit()


    @staticmethod
    def delete_image(image_id: uuid.UUID):
        with get_db_session() as db_session:
            image_to_delete = db_session.query(Image).filter(Image.id == image_id).one_or_none()
            if image_to_delete:
                db_session.delete(image_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Image with id {image_id} not found')    

    @staticmethod
    def get_image_by_product_id(product_id: int):
        pass

    # Получение изображения конкретного товара (по id товара)
    @staticmethod
    def get_image_by_product_id(product_id: int):
        pass

    # Изменение изображения (на вход подается id изображения и новая строка для замены)
    @staticmethod
    def change_image(image_id: uuid.UUID, byte_array: bytes):
        pass
