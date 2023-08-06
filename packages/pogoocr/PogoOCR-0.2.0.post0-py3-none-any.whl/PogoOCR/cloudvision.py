from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account


class Image:
    def __init__(self, service_file, image_content=None, image_uri=None):
        self.google = vision.ImageAnnotatorClient(
            credentials=service_account.Credentials.from_service_account_file(
                service_file
            )
        )

        self.image = types.Image()
        if image_content:
            self.image.content = image_content
        elif image_uri:
            self.image.source.image_uri = image_uri
        else:
            raise AttributeError("Please define either image_uri or image_content")

    def get_text(self):
        print(
            "Requesting TEXT_DETECTION from Google Cloud API. This will cost us 0.0015 USD."
        )
        response = self.google.text_detection(image=self.image)
        self.text_found = response.text_annotations
