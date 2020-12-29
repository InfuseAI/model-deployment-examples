from PIL import Image
from io import BytesIO
import numpy as np

class MyModel(object):
  def __init__(self):
    print('calling init()...')

  def predict(self, request, names=None, meta=None):
    print('calling predict()...')
    imageStream = BytesIO(request)
    image = Image.open(imageStream).resize((128, 128)).convert('L')
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()
