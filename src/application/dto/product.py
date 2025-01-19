from datetime import date
import json
from uuid import UUID


class ProductDTO:
    def __init__(self, id: int | None, name: str, category: str, price: int, available_stock: int, last_update_date: date, supplier_id: int, image_id: UUID):
        self.id = id
        self.name = name
        self.category = category
        self.price = price
        self.available_stock = available_stock
        self.last_update_date = last_update_date.isoformat()
        self.supplier_id = supplier_id
        self.image_id = image_id

    def map_product_dto_to_json(self):
        return json.dumps(self.__dict__)
