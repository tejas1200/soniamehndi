import base64
import requests
from django.conf import settings


def upload_to_imagekit(file):

    encoded_file = base64.b64encode(
        file.read()
    ).decode("utf-8")

    response = requests.post(
        "https://upload.imagekit.io/api/v1/files/upload",
        auth=(settings.IMAGEKIT_PRIVATE_KEY, ""),
        data={
            "file": encoded_file,
            "fileName": file.name
        }
    )

    data = response.json()

    if response.status_code != 200:
        raise Exception(data)

    return data["url"]