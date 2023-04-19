import io
from PIL import Image
import base64
import requests

image = Image.open('gtacam.jpeg')
image_byte_arr = io.BytesIO()
image.save(image_byte_arr, format='JPEG', subsampling=0, quality=100)
image_byte_arr = base64.b64encode(image_byte_arr.getvalue())
print("image converted")

url = 'http://10.0.0.152:8000/process_data'
myobj = {'body': image_byte_arr}
x = requests.post(url, json = myobj)
