"""Python binding for CSM API."""
import ec_config
ENDPOINT = 'http://localhost:{}'.format(ec_config.CSM_PORT)

import requests

# example
profile = {
    'd_name': 'D1',
    'dm_name': 'MorSensor',
    'u_name': 'yb',
    'is_sim': False,
    'df_list': ['Acceleration', 'Temperature'],
}
mac_addr = 'C860008BD249'
#csmapi.register(csmapi.mac_addr, csmapi.profile)
#register(mac_addr, profile)

class CSMError(Exception):
    pass


def register(mac_addr, profile):
    r = requests.post(
        ENDPOINT + '/' + mac_addr,
        json = {'profile': profile},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True

def deregister(mac_addr):
    r = requests.delete(ENDPOINT + '/' + mac_addr)
    if r.status_code != 200: raise CSMError(r.text)
    return True

def push(mac_addr, df_name, data):
    r = requests.put(
        ENDPOINT + '/' + mac_addr + '/' + df_name,
        json = {'data': data},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True

def pull(mac_addr, df_name):
    r = requests.get(ENDPOINT + '/' + mac_addr + '/' + df_name)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['samples']

def tree():
    r = requests.get(ENDPOINT + '/tree')
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()

def get_alias(mac_addr, df_name):
    r = requests.get(ENDPOINT + '/get_alias/' + mac_addr + '/' + df_name)
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['alias_name']

##### DF-module part #####
# dfo_id == 0 means join
# 不是我喜歡用 + 來串字串，是因為這樣寫某人比較好理解。
def dfm_push(na_id, dfo_id, stage, data):
    r = requests.put(
        ENDPOINT + '/dfm/' + str(na_id) + '/' + str(dfo_id) + '/' + stage,
        json = {'data': data},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True

def dfm_pull(na_id, dfo_id, stage):
    r = requests.get(
        ENDPOINT + '/dfm/' + str(na_id) + '/' + str(dfo_id) + '/' + stage,
    )
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['samples']

def dfm_push_min_max(na_id, dfo_id, stage, min_max):
    r = requests.put(
        ENDPOINT + '/dfm/' + str(na_id) + '/' + str(dfo_id) + '/' + stage + '/min_max',
        json = {'min_max': min_max},
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True

def dfm_pull_min_max(na_id, dfo_id, stage):
    r = requests.get(
        ENDPOINT + '/dfm/' + str(na_id) + '/' + str(dfo_id) + '/' + stage + '/min_max',
    )
    if r.status_code != 200: raise CSMError(r.text)
    return r.json()['min_max']

def dfm_reset(na_id, dfo_id):
    r = requests.delete(
        ENDPOINT + '/dfm/' + str(na_id) + '/' + str(dfo_id)
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True

def dfm_reset_all():
    r = requests.delete(
        ENDPOINT + '/dfm/'
    )
    if r.status_code != 200: raise CSMError(r.text)
    return True
