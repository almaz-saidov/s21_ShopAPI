import json

from application.models.image import Image


class ImageDTO:
    def __init__(self, image: Image):
        self.id = image.id
        self.data = image.data

    def map_image_dto_to_json(self):
        return json.dumps(self.id)
