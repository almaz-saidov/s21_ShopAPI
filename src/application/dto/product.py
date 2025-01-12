import json

from application.models.product import Product


class ProductDTO:
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.category = product.category
        self.price = product.price
        self.available_stock = product.available_stock
        self.last_update_date = product.last_update_date.isoformat()
        self.supplier_id = product.supplier_id
        self.image_id = product.image_id

    def map_product_dto_to_json(self):
        return json.dumps(self.__dict__)
