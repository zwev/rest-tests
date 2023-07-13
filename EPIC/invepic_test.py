from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check
import time
import sys

sys.path.append('..')
from common.shared import factory_reset

key = """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251"""

select_settings = {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}
RF_settings = {'rfmode': '1',}
invtime = 10
on = {
"mode": 0,
"enabled": True
}
off = {
"mode": 0,
"enabled": False
}
epic = False


def selposter(args, payload):
    response = requests.post(
         "{}/***/v0/rain/sel".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args['timeout']
         )
    print(response.status_code)

def RFposter(args, payload):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']},
         json=payload,
         timeout=args['timeout']
         )
    print(response.status_code)

def RFgetter(args, payload):
    response = requests.get(
         "{}/***/v0/rain/rfmode".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout']
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def selgetter(args, payload):
    response = requests.get(
         "{}/***/v0/rain/sel".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout']
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def epicgetter(args):
    global epic
    response = requests.get(
         "{}/***/v0/epic".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}
         )
    response_body = response.json()
    print(json.dumps(response_body, indent=2))
    if response_body['enabled'] == True:
        epic = True
    else:
        epic = False

    #check.equal(payload, response_body, message)

def keyposter(args, payload):
    response = requests.post(
         "{}/***/v0/epic/key".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, data=payload
         )
    #if err == response.status_code:
        #getter(message,payload)
    #else:
        #check.equal(202, 400)
        #print(message, response.status_code)
    #response_body = response.json()
    print(response.status_code)

def modeposter(args, payload):
    response = requests.post(
         "{}/***/v0/epic".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload
         )
    #if err == response.status_code:
        #getter(message,payload)
    #else:
        #check.equal(202, 400)
        #print(message, response.status_code)
    #response_body = response.json()
    print(response.status_code)

def invstart(args):
    response = requests.get(
         "{}/***/v0/inv/start".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout']
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2), response.status_code)
    #check.equal(payload, response_body, message)

def invstop(args):
    response = requests.get(
         "{}/***/v0/inv/stop".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout']
         )
    response_body = response.json()
    pc_list = []
    epc_list = []
    for item in response_body:
        print(item["epc"], item["pc"])
        pc_list.append(item["pc"])
    if epic == True:
        print(epic)
        check.is_not_in('4155', pc_list, "EPIC tags should all be unencrypted")
    else:
        print(epic)
        check.is_in('4155', pc_list, "EPIC tags should all be encrypted")

def delete(args):
    response = requests.delete("{}/***/v0/epic/key".format(args['ip']),
         headers={"Authorization": "Bearer " + args['serial']})
    print(response.status_code)


def test(ip, serial, tout, do_reset):
    args = {"ip": ip, "serial": serial, "timeout": tout}

    selposter(args, select_settings)
    selgetter(args, select_settings)
    RFposter(args, RF_settings)
    RFgetter(args, RF_settings)
    epicgetter(args)
    invstart(args)
    time.sleep(invtime)
    invstop(args)
    modeposter(args, on)
    keyposter(args, key)
    epicgetter(args)
    invstart(args)
    time.sleep(invtime)
    invstop(args)
    delete(args)
    modeposter(args, off)