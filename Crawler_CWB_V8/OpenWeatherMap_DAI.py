# DAI.py #coding=utf-8 -- new version of Dummy Device DAI.py, modified by tsaiwn@cs.nctu.edu.tw
import time, Crawler_CWB_V8.DAN as DAN, requests, random 
import threading, sys # for using a Thread to read keyboard INPUT
import requests, json 
from pprint import pprint


ServerURL = 'https://2.iottalk.tw' 

Reg_addr = None 

mac_addr = 'CD8600D38' + str( 517 ) 

Reg_addr = mac_addr  
DAN.profile['dm_name']='w_weather'   # you can change this but should also add the DM in server
DAN.profile['df_list']=['hscli_Pressure_I', 'hscli_Humidity_I', 'hscli_Temperature_I', 'hscli_WindSpeed_I', 'hscli_WeatherDes_I', 'hscli_UV_I', 'hscli_FeelsLike_I']   # Check IoTtalk to see what IDF/ODF the DM has
DAN.profile['d_name']= "HSCLi_."+ "Hsinchu" +"_"+ DAN.profile['dm_name'] # None
DAN.device_registration_with_retry(ServerURL, Reg_addr) 
print("dm_name is ", DAN.profile['dm_name']) ; print("Server is ", ServerURL)

# Enter your API key here 
api_key = "2f634d46796850dcc4c3a54a254759d9"
  
# base_url variable to store url 
#base_url = "http://api.openweathermap.org/data/2.5/weather?" ver. 1.0
base_url = "http://api.openweathermap.org/data/2.5/onecall?" #ver. 2.0


#city_name = "Hsinchu,TW"
latitude = "24.7857152"
longitude = "120.995840"
#latitude = "-36.5200"
#longitude = "174.460000"
  
# complete_url variable to store 
# complete_url = base_url + "appid=" + api_key + "&q=" + city_name ver. 1.0
complete_url = base_url +"lat="+latitude+"&lon="+longitude +"&exclude=hourly,daily,minutely&appid=" + api_key +"&lang=zh_tw&units=metric" #ver. 2.0
  
# get method of requests module return response object 
response = requests.get(complete_url) 

x = response.json() 
pprint(x)
 
y = x["current"] 
# store the value corresponding to the specific key of y 
current_temperature = y["temp"]
current_feelslike = y["feels_like"]
current_pressure = y["pressure"] 
current_humidity = y["humidity"] 
current_windspeed = y["wind_speed"] 
current_uvi = y["uvi"]
z = x['current']['weather']
weather_description = z[0]['description']


def GetOpenWeatherMapData():
    response = requests.get(complete_url) 
    x = response.json() 
    y = x["current"] 
    current_temperature = y["temp"]
    current_feelslike = y["feels_like"]
    current_pressure = y["pressure"] 
    current_humidity = y["humidity"] 
    current_windspeed = y["wind_speed"] 
    current_uvi = y["uvi"]
    z = x['current']['weather']
    weather_description = z[0]['description']
    # Print out to see if it is correct
    print("current:", weather_description ,"humid:", current_humidity,"pressure:",current_pressure,"temp:",current_temperature,"wind:",current_windspeed, "feelslike:", current_feelslike, "uv:",current_uvi)

def PushDataToIottalk(data):
    print("pull")
    DAN.push('AtPressure', data['海平面氣壓(百帕)'])
    # time.sleep(1)
    DAN.push ('Humidity1',  data['相對溼度'] )  #  試這:  DAN.push('Dummy_Sensor', theInput) 
    # time.sleep(1)
    DAN.push ('Temperature1', data['溫度(℃)'])
    # time.sleep(1)
    DAN.push ('Time1', data['觀測時間'])
    # time.sleep(1)
    DAN.push ('View', data['能見度(公里)'])
    # time.sleep(1)
    DAN.push ('Weather', data['天氣'])
    # time.sleep(1)
    DAN.push ('Wind1', data['風力(m/s)'])
    # time.sleep(1)
    DAN.push ('Wind2', data['陣風(m/s)'])
    # time.sleep(1)
    DAN.push ('Winddr', data['陣風(m/s)'])
    # time.sleep(1)
    DAN.push ('rain', data['陣風(m/s)'])
    # time.sleep(1)
    DAN.push ('sun', data['陣風(m/s)'])
    # time.sleep(1)

GetOpenWeatherMapData()
while True:
    try:
      GetOpenWeatherMapData()
      #Push as inputs of IDF
      PushDataToIottalk()
      time.sleep(5) # change to your suitable use
    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    
    except KeyboardInterrupt:
       break

try: 
   DAN.deregister()    # 試著解除註冊
except Exception as e:
   print("===")
print("Bye ! --------------", flush=True)
sys.exit( )