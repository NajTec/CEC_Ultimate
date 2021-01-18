import threading
import time
import sys
import random
import webview
from cassandra.cluster import Cluster



cluster = Cluster(['myhsiotaci.eastus.azurecontainer.io'],port=9042)
session = cluster.connect('mykeyspace')
rows = session.execute('SELECT * FROM full_log')
length = session.execute('SELECT count(*) FROM full_log')

run = True
x = [rows[i].zeitstempel for i in range(0,10)]
y = [rows[i].humidity for i in range(0,10)]

class Api:
    def init(self):
        global x, y

        response = {
            'x': x,
            'y': y,
        }

        return response
    
    def send_data(self, x, y):
        return {'x': x, 'y':y}

    def log(self, str):
        print(str)

def Gui():
    with open('index.html', 'r') as file:
        html = file.read().replace('\n', '')

    api = Api()
    window = webview.create_window('API example', html=html, js_api=api)

    def updateGraph(index: int, x: list, y: list):
        xstr = str(x)
        ystr = str(y)
        idxstr = str(index)

        window.evaluate_js(
            """
            myChart.data.labels="""+xstr+""";

            myChart.data.datasets["""+idxstr+"""].data="""+ystr+""";
            myChart.update();
            """
        ) 

    def thread_function(name):
        global run, api, x, y

        while run:
            time.sleep(0.1)
            api.send_data(x, y)

            x.append(x[-1]+1)
            y.append(random.randrange(10))

            updateGraph(0, x, y)
            updateGraph(1, x, y)

            # print(y)
            # print(x)


if __name__ == '__main__':
    #window = webview.create_window('API example', html=html, js_api=api)
    Gui()
    th = threading.Thread(target=thread_function, args=(1,))
    th.start()

    webview.start(debug=True)
    #run=False