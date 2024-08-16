import time, random, requests
import DAN
import crawl_weather_V8 as cw
import os
import csv

ServerURL = 'https://2.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = '1000.1'

DAN.profile['dm_name']='qazwer'
DAN.profile['df_list']=['date', 'temp', 'weather', 'wind_direction', 'wind_speed', 'gust_wind', 'visible', 'hum', 'pre', 'rain', 'sunlight']
DAN.profile['d_name']= 'qazwer_device' 

DAN.device_registration_with_retry(ServerURL, Reg_addr)
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line

while True:
    try:
        cw.crawl_w()
        csv_file = './Hsinchu.csv'
        with open(csv_file, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            for data in csv_reader:
                if data[0] == '0':
                    for i, f in enumerate(DAN.profile['df.list']):
                        time.sleep(1)
                        DAN.push(f, data[i+1])
                        print(f, data[i+1])
                    break
        # ODF_data = DAN.pull('Dummy_Control')#Pull data from an output device feature "Dummy_Control"
        # if ODF_data != None:
        #     print (ODF_data[0])

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(1)

