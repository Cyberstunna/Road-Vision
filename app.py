import falcon, cv2
import numpy
import os
import base64
import io
from PIL import Image
from .image_processor import ReadLicensePlate

class GTACamerasEndpoint:
    def on_post(self, req, resp):
        imageByteArray = req.media["body"]
        imageByteArray = base64.b64decode(imageByteArray)
        #imageByteArray = data["body"].decode('base64')
              
        image = Image.open(io.BytesIO(imageByteArray))
        image.save("Car.jpeg")
        
        # Convert the array to make a 400x300 grayscale image.
        # grayImage = flatNumpyArray.reshape(300, 400)
        #cv2.imwrite('Car.png', grayImage)
        result = ReadLicensePlate().check_image("Car.jpeg")
      
        resp.text = {"result": result}
        resp.status = falcon.HTTP_OK
        resp.content_type = falcon.MEDIA_JSON
        
    def on_get(self, req, resp):
        queryPlate, queryTime = req["body"]

        #function call to search mongodb goes here
        #
        #
        #
        result = False

        if result:
            resp.text = {"times": ["Array of timestamps it was found"], "images": ["Array of image byte arrays to be converted at the dashboard"]}
            resp.status = falcon.HTTP_200
            resp.content_type = falcon.MEDIA_JSON
        else:
            resp.text = {"message": "Could not find record"}
            resp.status = falcon.HTTP_404
            resp.content_type = falcon.MEDIA_JSON
    
app = application = falcon.App()

endpoint = GTACamerasEndpoint()
app.add_route("/search_data", endpoint)
app.add_route("/process_data", endpoint)