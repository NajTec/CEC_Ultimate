from cassandra.cluster import Cluster
import matplotlib.pyplot as plt
from time import sleep
import time
from datetime import datetime
import operator
from matplotlib.animation import FuncAnimation

cluster = Cluster(['myhsiotaci.southcentralus.azurecontainer.io'],port=9042)
session = cluster.connect('mykeyspace')
ln, = plt.plot([], [], 'ro')
fig, ax = plt.subplots()
lis1,lis2 = [],[]

 

def datetimegen(row):
    return datetime.strptime(row.zeitstempel[:-5],'%Y-%m-%dT%H:%M:%S')



while(1):
    rows = session.execute('SELECT * FROM full_log')
    length = session.execute('SELECT count(*) FROM full_log')
    length = length[0].count
    print(length)
    print(rows[0].zeitstempel[11:-5])
    x = [datetimegen(rows[i]) for i in range(0,10)]
    y = [rows[i].humidity for i in range(0,10)]
    lis = sorted(zip(x,y),key=operator.itemgetter(0))
    lis1,lis2 = zip(*lis)
    print( lis[0] )    
    print(lis[1])
    plt.xlabel("Timestamp")
    plt.ylabel("Humidity")
    plt.grid(True)
    f1.set_xdata(lis1)
    f1.set_ydata(lis2)
    plt.draw()

    #sleep(1)