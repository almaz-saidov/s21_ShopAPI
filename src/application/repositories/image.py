from datetime import date
import uuid

from sqlalchemy import update
from werkzeug.exceptions import NotFound

from application.database import get_db_session
from application.dto.image import ImageDTO
from application.models import Image, Product


class ImageRepository:
    def add_image(self, image_dto: ImageDTO, product_id: int):
        with get_db_session() as db_session:
            product_to_add_image = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product_to_add_image:
                raise NotFound(f'Product with id {product_id} not found')
            
            if product_to_add_image.image_id:
                raise Exception(f'Product with id {product_id} already has image')
            
            new_image = Image(id=uuid.uuid4(), data=image_dto.data)
            db_session.add(new_image)
            
            query = update(Product).where(Product.id == product_to_add_image.id).values(image_id=new_image.id, last_update_date=date.today())
            db_session.execute(query)
            
            db_session.commit()

    def delete_image(self, image_id: uuid.UUID):
        with get_db_session() as db_session:
            image_to_delete = db_session.query(Image).filter(Image.id == image_id).one_or_none()
            
            if not image_to_delete:
                raise NotFound(f'Image with id {image_id} not found')    
            
            db_session.delete(image_to_delete)
            db_session.commit()

    def get_image_by_id(self, image_id: uuid.UUID):
        with get_db_session() as db_session:
            image = db_session.query(Image).filter(Image.id == image_id).one_or_none()
            
            if not image:
                raise NotFound(f'Image with id {image_id} not found')
            
            return image.data

    def get_image_by_product_id(self, product_id: int):
        with get_db_session() as db_session:
            product = db_session.query(Product).filter(Product.id == product_id).one_or_none()
            
            if not product:
                raise NotFound(f'Product with id {product_id} not found')
            
            if not product.image_id:
                raise Exception(f'Product with id {product_id} has no image')
            
            image = db_session.query(Image).filter(Image.id == product.image_id).one_or_none()
            return image.data

    def change_image(self, image_dto: ImageDTO):
        with get_db_session() as db_session:
            image_to_change = db_session.query(Image).filter(Image.id == image_id).one_or_none()
            
            if not image_to_change:
                raise NotFound(f'Image with id {image_dto.id} not found')
            
            query = update(Image).where(Image.id == image_dto.id).values(data=image_dto.data)
            db_session.execute(query)
            
            db_session.commit()
