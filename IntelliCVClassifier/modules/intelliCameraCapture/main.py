#!/usr/bin/python3
import os
import uuid
import sys
import random
from azure.storage.blob import BlockBlobService, PublicAccess

import time
from progress.bar import IncrementalBar

import time
# import sys
# import os
import subprocess
import requests
import json
from azure.iot.device import IoTHubModuleClient, Message

# global counters
SENT_IMAGES = 0

# global client
CLIENT = None

# Send a message to IoT Hub
# Route output1 to $upstream in deployment.template.json
def send_to_hub(strMessage):
    message = Message(bytearray(strMessage, 'utf8'))
    CLIENT.send_message_to_output(message, "output1")
    global SENT_IMAGES
    SENT_IMAGES += 1
    print( "Total images sent: {}".format(SENT_IMAGES) )

# Send an image to the image classifying server
# Return the JSON response from the server with the prediction result
def sendFrameForProcessing(imagePath, imageProcessingEndpoint):
    headers = {'Content-Type': 'application/octet-stream'}

    with open(imagePath, mode="rb") as test_image:
        try:
            response = requests.post(imageProcessingEndpoint, headers = headers, data = test_image)
            # print("Response from classification service: (" + str(response.status_code) + ") " + json.dumps(response.json(), indent=2, sort_keys=True) + "\n")
            #
            predictions = response.json()["predictions"]
            classify(predictions[0]["probability"], predictions[1]["probability"], predictions[2]["probability"])
        except Exception as e:
            print(e)
            print("No response from classification service")
            return None

    return json.dumps(response.json())

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#def showBar(label, num):
#    bar = IncrementalBar(label, max = 100_000, suffix='%(percent)f%%')
#    for i in range(num):
#        bar.next()
#    bar.finish()
#print('\n')

def classify(d, e, s):
    # mySet = (d, e, s)
    # mySet = list(int(el*100_000) for el in mySet)
    #showBar('Diskozyt', mySet[0])
    #showBar('Echinozyt', mySet[1])
    #showBar('Sphaerozyt', mySet[2])
    print("Diskozyt: " + str(d) + "%")
    print("Echinozyt: " + str(e) + "%")
    print("Sphaerozyt: " + str(s) + "%")

def main(imageProcessingEndpoint):
    try:
        print ( "Simulated camera module for Azure IoT Edge. Press Ctrl-C to exit." )

        try:
            global CLIENT
            CLIENT = IoTHubModuleClient.create_from_edge_environment()
        except Exception as iothub_error:
            print ( "Unexpected error {} from IoTHub".format(iothub_error) )
            return

        print ( "The sample is now sending images for processing and will indefinitely.")

        while True:
            imagePath = get_image_from_blob()
            classification = sendFrameForProcessing(imagePath, imageProcessingEndpoint)
            if classification:
                send_to_hub(classification)
            time.sleep(10)
            os.remove(imagePath)

    except KeyboardInterrupt:
        print ( "IoT Edge module sample stopped" )


def get_image_from_blob():
    try:
        # Create the BlockBlobService that is used to call the Blob service for the storage account
        blob_service_client = BlockBlobService(
            account_name='intellisave', account_key='7Qh8L1ATZ5cDP+BXUcMXUMzQa3llFJhXn9C21bxLL/KCQUCFHS5hMR2nmXH7SopXIK/gbtzMpt2baoSYT+TvEw==')

        # Create a container called 'quickstartblobs'.
        container_name = 'intelli-save-container'

        # Set the permission so the blobs are public.
        blob_service_client.set_container_acl(
            container_name, public_access=PublicAccess.Container)

        # Create capturedImages folder if it not exists
        local_path = os.path.expanduser("./capturedImages")
        if not os.path.exists(local_path):
            os.makedirs(os.path.expanduser("./capturedImages"))
        
        # List the blobs in the container
        blob_files = [el for el in blob_service_client.list_blobs(container_name)]
        print(blob_files)

        # Download the blob.
        rand_id = random.randrange(len(blob_files))
        blob_name = blob_files[rand_id].name
        # print(blob_name)
        full_path_to_file = os.path.join(local_path, blob_name)


        print("\nDownloading blob to " + full_path_to_file)
        blob_service_client.get_blob_to_path(
            container_name, blob_name, full_path_to_file)
        
        return full_path_to_file

    except Exception as e:
        print(e)


if __name__ == '__main__':
    install("azure.storage.blob==2.1.0")
    try:
        # Retrieve the image location and image classifying server endpoint from container environment
        # IMAGE_PATH = os.getenv('IMAGE_PATH', "")
        #IMAGE_PROCESSING_ENDPOINT = os.getenv('IMAGE_PROCESSING_ENDPOINT', "")
        IMAGE_PROCESSING_ENDPOINT = "http://classifier/image"
    except ValueError as error:
        print ( error )
        sys.exit(1)

    if ((IMAGE_PROCESSING_ENDPOINT) != ""):
        main(IMAGE_PROCESSING_ENDPOINT)
    else: 
        print ( "Error: Image path or image-processing endpoint missing" )