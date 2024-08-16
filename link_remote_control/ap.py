from flask import Flask
from flask import render_template
from flask import make_response
import csmapi
csmapi.ENDPOINT = 'https://2.iottalk.tw'
app = Flask(__name__)
htmlname = "Bus Website"
name="myFlask"
varinPython="158"


@app.route("/bus", methods=['GET'])
def bus_html():
   return make_response(render_template('bus.html', methods=['GET']))
@app.route("/RC/<device_id>/", methods=['GET'])
def remote_control_generator(device_id):
    sync = request.args.get('sync')
    if sync != 'True': sync = False
    def register_remote_control(device_id):
        profile = {
            'd_name': device_id,
            'dm_name': 'Remote_control',
            'u_name': 'yb',
            'is_sim': False,
            'mqtt_enable': ec_config.MQTT_enable,
            'df_list': [],
        }
        for i in range(1,26):
            profile['df_list'].append("Keypad%d" % i)
            profile['df_list'].append("Button%d" % i)
            profile['df_list'].append("Switch%d" % i)
            profile['df_list'].append("Knob%d" % i)
            profile['df_list'].append("Color-I%d" % i)
            profile['df_list'].append("Toggle%d" % i)
            profile['df_list'].append("Slider%d" % i)
        try:        
            result = csmapi.register(device_id, profile)
            if result: print('Remote control generator: Remote Control successfully registered.')
            return result
        except Exception as e:
                print('Remote control generator: ', e)
    
        profile = None
        try:    
            profile = uds.pull(device_id, 'profile')
        except Exception as e:
            print('Remote control generator: ', e)
            if str(e).find('mac_addr not found:') != -1:
                print('Remote control generator: Register Remote Control...')
                result = register_remote_control(device_id)
                return 'Remote control "'+device_id+'" successfully registered. <br> Please bind it in the IoTtalk GUI.', 200
            else:
                print('Remote control generator: I dont know how to handel this error. Sorry...pass.')
                abort(404)
    
        if profile:
            try:
                Ctl_O = uds.pull(device_id, '__Ctl_O__')
            except Exception as e:
                print('Remote control generator: ', e)
                abort(404)
    
            if Ctl_O != []:
                selected_df_flags = Ctl_O[0][1][1]['cmd_params'][0]
            
                df_list = profile['df_list']
                df_dict = {'Butt': 0, 'Colo': 0, 'Keyp': 0, 'Knob': 0, 'Swit': 0, 'Togg':0, 'Slid':0}
    
                for index, element in list(enumerate(selected_df_flags)):
                    if element == '1': df_dict[df_list[index][:4]] += 1
                MQTT_ENABLE = False
                if ec_config.MQTT_enable == True: MQTT_ENABLE = 'true'
                else: MQTT_ENABLE = 'false'
                return make_response(render_template('remotecontrol.html', device_id=device_id, df_dict=df_dict, sync=sync, mqtt_enable=MQTT_ENABLE))
                
            else:
                print('Remote control generator: Ctl_O is empty.')
                return 'Please bind this remote control "'+device_id+'" in the IoTtalk GUI.', 200
    
        else:  
            print('Remote control generator: Profile is empty.')
            abort(404)
    
   
@app.route("/Bus")
def bushtml( ):
   return render_template( 'bus.html',name=name, ggyy=varinPython)