from application.database import get_db_session
from sqlalchemy.dialects.postgresql import UUID

from application.models import Image, Product


class ImageORM:
    # добавление изображения (на вход подается byte array изображения и id товара).
    @staticmethod
    def add_image(byte_array: bytes, product_id: int):
        pass

    @staticmethod
    def delete_image(image_id: UUID):
        with get_db_session() as db_session:
            image_to_delete = db_session.query(Image).filter(Image.id == image_id).one_or_none()
            if image_to_delete:
                db_session.delete(image_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Image with id {image_id} not found')    

    # Получение изображения по id изображения
    @staticmethod
    def get_image_by_product_id(id: UUID):
        pass

    # Получение изображения конкретного товара (по id товара)
    @staticmethod
    def get_image_by_product_id(product_id: int):
        pass

    # Изменение изображения (на вход подается id изображения и новая строка для замены)
    @staticmethod
    def change_image(id: UUID, byte_array: bytes):
        pass
