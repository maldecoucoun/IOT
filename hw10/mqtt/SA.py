import random 
import time
import numpy as np

ServerURL = 'https://class.iottalk.tw' #For example: 'https://DomainName'
MQTT_broker = 'class.iottalk.tw' # MQTT Broker address, for example: 'DomainName' or None = no MQTT support
MQTT_port = 1883
MQTT_encryption = False
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'Dummy_Device'
IDF_list = ['Dummy_Sensor']
ODF_list = ['Dummy_Control']
device_id = None #if None, device_id = MAC address
device_name = None
exec_interval = 1  # IDF/ODF interval

delays = []

def Dummy_Sensor():
    return time.perf_counter()

def Dummy_Control(data:list):
    end = time.perf_counter()
    start = data[0]
    delays.append(end -start)
    print(end - start)

    if len(delays) == 100:
        avg = np.mean(delays)
        std = np.std(delays)
        cv = std/avg
        print("avg: ", avg)
        print("cv: ", cv)

def on_register(r):
    print(f'Device name: {r["d_name"]}')    
    '''
    #You can write some SA routine code here, for example: 
    import time, DAI
    while True:
        DAI.push('Dummy_Sensor', [100, 200])  
        time.sleep(exec_interval)    
    '''


