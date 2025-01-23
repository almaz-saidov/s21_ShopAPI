import json
from uuid import UUID


class ImageDTO:
    def __init__(self, id: UUID | None, data: bytes):
        self.id = id
        self.data = data

    def map_image_dto_to_json(self):
        return json.dumps(self.id)
