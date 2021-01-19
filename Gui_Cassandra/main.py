import threading
import time
import sys
import random
import webview
import json
from cassandra.cluster import Cluster

# cluster = Cluster(['myhsiotaci.westus.azurecontainer.io'],port=9042)
cluster = Cluster(['myhsiotaci.eastus.azurecontainer.io'],port=9042)
session = cluster.connect('mykeyspace')

run = True

datasets = []

class Dataset:
    x: list
    y: list


class Api:
    def init(self):
        global datasets

        response = {
            'x': datasets[0]["x"],
            'y': datasets[0]["y"],
        }

        return response
    
    def send_data(self, x, y):
        return {'x': x, 'y':y}

    def log(self, str):
        print(str)


def updateGraph(index: int, t: list, y: list):
    tstr = str([f"new Date('{time}')" for time in t]).replace('"', '')
    # tstr = str(t)
    ystr = str(y)
    idxstr = str(index)

    code = f"""
        myChart.data.datasets[{index}].label = 'Edge Nr. {index}';
        myChart.data.labels={tstr};
        // myChart.data.datasets[{idxstr}].data = {{t: {tstr},y: {ystr}}};
        myChart.data.datasets[{idxstr}].data={ystr};
        myChart.update();
        """
    #myChart.data.datasets[{idxstr}].data.push(\{t:new Date({tstr}), y: {ystr}\})
    window.evaluate_js(code) 

def thread_function(name):
    global run
    while run:
        time.sleep(1)
        
        rows = session.execute('SELECT * FROM full_log')
        length  = session.execute('SELECT count(*) FROM full_log')[0].count
        print("######################## length:"+ str(type(length)))
        print("######################## length:"+ str(length))

        print("1")
        device_1_x = [rows[i].zeitstempel for i in range(length-20,length)]
        print("2")
        device_1_y = [rows[i].humidity for i in range(length-20,length)]
        print("3")
        device_2_x = [rows[i].zeitstempel for i in range(length-20,length)]
        print("4")
        device_2_y = [rows[i].temperature for i in range(length-20,length)]
        print("5")

        print("\n")
        print(device_1_x)
        print(device_2_x)
        print("\n")

        updateGraph(0, device_1_x, device_1_y)
        updateGraph(1, device_2_x, device_2_y)


def stop_forward_thread():
    global run
    run = False


if __name__ == '__main__':
    # init with testvalues
    datasets.append(
    {
        'x':[1, 2, 3, 4, 5, 6, 7, 8],
        'y':[2, 1, 2, 3, 4, 1, 3, 8]
    })
    datasets.append(
    {
        'x':[1, 2, 3, 4, 5, 6, 7, 8],
        'y':[2, 1, 2, 3, 4, 1, 3, 8]
    })

    # Read HTML
    with open('index.html', 'r') as file:
        html = file.read().replace('\n', '')

    # Create API Obj
    api = Api()
    window = webview.create_window('API example', html=html, js_api=api)

    # Create Push Obj
    th = threading.Thread(target=thread_function, args=(1,))
    th.start()

    # Start GUI
    webview.start(debug=True) # Blocking
    stop_forward_thread()
