import time, random, requests
import DAN
import numpy as np
ServerURL = 'https://class.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None #if None, Reg_addr = MAC address

DAN.profile['dm_name']='Dummy_Device'
DAN.profile['df_list']=['Dummy_Sensor', 'Dummy_Control',]
DAN.profile['d_name']= '1588' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line


delays = []
i = 1
while True:
    try:
        # IDF_data = random.uniform(1, 10)
        start = time.perf_counter()
        DAN.push ('Dummy_Sensor', i) #Push data to an input device feature "Dummy_Sensor"

        #==================================

        ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        end = time.perf_counter()
        
        if ODF_data != None:
            delays.append(end - start)
            print (ODF_data[0])
            i += 1
            if i > 100:
                break

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)

avg = np.mean(delays)
std = np.std(delays)
cv = std/avg
print("avg: ", avg)
print("cv: ", cv)