
import os
import base64
import requests
from django.conf import settings

from visualiser import models


GOOGLE_VISION_API = ('https://vision.googleapis.com/v1/images:annotate?'
                     'key={}'.format(settings.GOOGLE_API_KEY))


MEDIA_DIR = 'media'

def get_image_data(image_content=False, image_url=False):
    body = {
        "requests": [
            {
                "image": {},
                "features": [
                    {
                        "type": "FACE_DETECTION"
                    },
                    {
                        "type": "TEXT_DETECTION"
                    },
                    {
                        "type": "LABEL_DETECTION"
                    }
                ]
            }
        ]
    }
    if image_content:
        body['requests'][0]['image']['content'] = image_content
    elif image_url:
        body['requests'][0]['image']['source'] = {'imageUri': image_url}
    else:
        return []
    response = requests.post(GOOGLE_VISION_API, json=body)
    response.raise_for_status()
    return response.json().get('responses')


def create_update_image(fp=False, image_url=False):
    if fp:
        image_path = upload_image(fp)
        image_content = encode_image(image_path)
        image_annotation = get_image_data(image_content=image_content)
        image_path = MEDIA_DIR + image_path.split(MEDIA_DIR)[1]
    elif image_url:
        image_path = image_url
        image_annotation = get_image_data(image_url=image_url)
    else:
        return []
    try:
        image = models.Image.objects.get_or_create(url=image_path)[0]
    except Exception as error:
        raise error

    for response in image_annotation:
        for label_annotation in response.get('labelAnnotations'):
            models.LabelAnnotation.objects.get_or_create(
                image=image, mid=label_annotation.get('mid', ''),
                score=label_annotation.get('score', 0.0),
                description=label_annotation.get('description', ''),
                topicality=label_annotation.get('topicality', 0.0))
        text = response.get('fullTextAnnotation', {}).get('text', '')
        if text:
            models.TextAnnotation.objects.get_or_create(image=image, text=text)

    data = {
        'labels': response.get('labelAnnotations'),
        'text': [tx for tx in text.split('\n') if tx]
    }
    return data


def upload_image(fp):
    fpath = os.path.join(os.path.realpath(str(settings.ROOT_DIR)),
                         ('dashboard/{}/{}'.format(MEDIA_DIR, fp.name)))
    with open(fpath, 'wb+') as dest:
        for chunk in fp.chunks():
            dest.write(chunk)
    return fpath


def encode_image(fpath):
    image_content = open(fpath, 'rb').read()
    return str(base64.b64encode(image_content), 'utf-8')
