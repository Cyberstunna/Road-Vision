from time import sleep, process_time
from paho.mqtt import client as mqtt
import ssl, re, os                              #SSL, RegEx, os for shutdown command
import socket
import hashlib
import io

from PIL import Image
import requests
path_to_root_cert = "./RecieveCerts/AmazonRootCA1.pem"                                  # local path to Amazon Root Cetificate
path_to_device_cert = "./RecieveCerts/gtacamdevicecert.pem.crt"         # local path to Device certificate pem or crt            
path_to_private_key = "./RecieveCerts/gtacamprivatekey.pem.key"                                # local path to Private key
device_id = "gta_camerar"
aws_url = "a1tw1id1vizft6-ats.iot.us-west-2.amazonaws.com"              # taken from AWS IoT Core

subscribe_topic = "image/reading"
subscribe_qos = 1

url = 'http://10.0.0.152:8000/process_data'                             # ip of server

def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Device disconnected with result code: " + str(rc))

def on_message(client, userdata, message):
    recmess = message.payload
    pyld, rechash = recmess.split(b'@#IOTproj#@')
    datahash = hashlib.sha256(pyld).hexdigest()
    rechash = rechash.decode("utf-8")

    if datahash == rechash:
        myobj = {'body': pyld}
        x = requests.post(url, json = myobj)
        print("Image sent to server.")
    else:
        print("Seems like the photos have been altered in transmission as the hashes don't match up")

    sleep(10)
   
def on_subscribe(client, userdata, mid, granted_qos):
    print("Client subscribed: ", str(mid), " with qos:", str(granted_qos))

def on_unsubscribe(client, userdata, mid):
    print("Client Unsubscribed")

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
awsClient.on_message = on_message
awsClient.on_subscribe = on_subscribe
awsClient.on_unsubscribe = on_unsubscribe

# create ssl context and settings (required for connection
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH,cafile=path_to_root_cert)
ssl_context.load_cert_chain(certfile=path_to_device_cert, keyfile=path_to_private_key)
awsClient.tls_set_context(context=ssl_context)
awsClient.tls_insecure_set(False)

# MQTT Client connect
awsClient.connect(aws_url, port=8883)
awsClient.loop_start()
sleep(5)
awsClient.subscribe((subscribe_topic, subscribe_qos))

while True:
    try:
        i = 1
    except KeyboardInterrupt:
        shut_down()
        break
