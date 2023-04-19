from time import sleep, process_time            #process_time is used for delays. Counts the running time of process
from paho.mqtt import client as mqtt
import ssl, os                              #SSL, os for shutdown command
import base64
import hashlib
import io
from PIL import Image
from json import dumps, loads

path_to_root_cert = "./SendCerts/AmazonRootCA1.pem"                                  # local path to Amazon Root Cetificate
path_to_device_cert = "./SendCerts/gtacamdevicecert.pem.crt"                                # local path to Device certificate pem or crt            
path_to_private_key = "./SendCerts/gtacamprivatekey.pem.key"                                # local path to Private key
device_id = "gta_cameras"
aws_url = "a1tw1id1vizft6-ats.iot.us-west-2.amazonaws.com"              # taken from AWS IoT Core

publish_topic = "image/reading"
publish_qos = 1

def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Device message sent.")
    shut_down()

def shut_down():
    print("System Exit initiated")
    awsClient.loop_stop()
    awsClient.disconnect()
    sleep(10)
    os._exit(0)

# MQTT Client definition
awsClient = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311)

# MQTT callback functions
awsClient.on_connect = on_connect
awsClient.on_disconnect = on_disconnect
awsClient.on_publish = on_publish

# create ssl context and settings (required for connection)
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH,cafile=path_to_root_cert)
ssl_context.load_cert_chain(certfile=path_to_device_cert, keyfile=path_to_private_key)
awsClient.tls_set_context(context=ssl_context)
awsClient.tls_insecure_set(False)

# MQTT Client connect
awsClient.connect(aws_url, port=8883)
awsClient.loop_start()
sleep(5)

#os.system('raspistill -q 100 -o gtacamraw.jpeg') #uncomment for photo-taking
#print("Image Taken")

image = Image.open('gtacamraw.jpeg') 
image = image.resize((400, 300), Image.ANTIALIAS)  
image.save('gtacam.jpeg') 

image = Image.open('gtacam.jpeg')                                      #converts image to byte array
image_byte_arr = io.BytesIO()
image.save(image_byte_arr, format='JPEG', subsampling=0, quality=100)
image_byte_arr = base64.b64encode(image_byte_arr.getvalue())
print("Image Converted to Byte Array")

imagehash = hashlib.sha256(image_byte_arr).hexdigest()
package = image_byte_arr + b'@#IOTproj#@' + imagehash.encode("utf-8")

awsClient.publish(publish_topic, package, qos=publish_qos)               #publishes image
sleep(10)

shut_down()