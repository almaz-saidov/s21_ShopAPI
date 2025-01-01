from sqlalchemy.dialects.postgresql import UUID

from application.models import Image, Product


class ImageORM:
    # добавление изображения (на вход подается byte array изображения и id товара).
    @staticmethod
    def add_image(byte_array: bytes, product_id: int):
        pass

    # Удаление изображения по id изображения
    @staticmethod
    def delete_image(id: UUID):
        pass    

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
