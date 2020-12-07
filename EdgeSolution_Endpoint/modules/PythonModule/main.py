# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

import random
import time
import requests
import json
import base64
import random
import os

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=myhsiothub.azure-devices.net;DeviceId=myEdgeDevice;SharedAccessKey=xZOUcdZGQTT/z/fAwX3/sKYSkCDrr1tPXsy6ysetLHM="

# Define the JSON message to send to IoT Hub.
MSG_TXT = '{{"Picture": {picture},"Bloodtype": {bloodtype}}}'
scoring_uri = 'http://0bfa3359-0d3b-4806-b2f6-11488f8515e6.westeurope.azurecontainer.io/score'
key = 'z7v89lmQSqZTpHgBcZsUqtIIgXvFDjKD'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

currentdir = os.path.dirname(os.path.realpath(__file__))
def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            pic = random.randrange(12)
            img_name =  currentdir + '/' + str(pic) + '.bmp'
            with open(img_name, 'rb') as f:
                encoded_string = base64.b64encode(f.read())
            
            img_data = encoded_string.decode("utf-8")
            data = { "Inputs" :
                {
                    "WebServiceInput0" : [
                    {
                        "image" : img_data,
                        "id" : 0,
                        "category" : "Discocytes-Test"
                    }
                    ]
                },
                "GlobalParameters": {}
            }
            input_data = json.dumps(data)

            headers = {'Content-Type' : 'application/json'}
            headers['Authorization'] = f'Bearer {key}'

            resp = requests.post(scoring_uri, input_data, headers=headers)
            print(resp.text)
            msg_txt_formatted = MSG_TXT.format(picture=resp.text, bloodtype="discocytes")
            message = Message(msg_txt_formatted)


            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()