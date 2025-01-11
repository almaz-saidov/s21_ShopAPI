import json

from application.models.image import Image


class ImageDTO:
    def __init__(self, image: Image):
        self.id = image.id

    def map_image_dto_to_json(self):
        return json.dumps(self.__dict__)
