# This test checks that if there is no epic key installed 

from socket import timeout
from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check
import time
import sys

sys.path.append('..')
from common.shared import factory_reset, ssl_reset

sec = "http://"

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


def selposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args['timeout'], verify=ver
         )
    print(response.status_code)

def RFposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']},
         json=payload,
         timeout=args['timeout'],verify=ver
         )
    print(response.status_code)

def RFgetter(args, payload, ver):
    response = requests.get(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def selgetter(args, payload, ver):
    response = requests.get(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def epicgetter(args, ver):
    global epic
    response = requests.get(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args['serial']},timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(json.dumps(response_body, indent=2))
    if response_body['enabled'] == True:
        epic = True
    else:
        epic = False


def keyposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/epic/key".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, data=payload, timeout=args['timeout'],verify=ver
         )
    print(response.status_code)

def modeposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload,timeout=args['timeout'], verify=ver
         )
    print(response.status_code)

def invstart(args, ver):
    response = requests.get(
         "{}/***/v0/inv/start".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()


def invstop(args, ver):
    response = requests.get(
         "{}/***/v0/inv/stop".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
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

def delete(args, ver):
    response = requests.delete("{}/***/v0/epic/key".format(sec),
         headers={"Authorization": "Bearer " + args['serial']},timeout=args['timeout'], verify=ver)
    print(response.status_code)


def test_epic_decoding(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    selposter(args, select_settings, ver)
    selgetter(args, select_settings, ver)
    RFposter(args, RF_settings, ver)
    RFgetter(args, RF_settings, ver)
    epicgetter(args, ver)
    invstart(args, ver)
    time.sleep(invtime)
    invstop(args, ver)
    keyposter(args, key, ver)
    modeposter(args, on, ver)
    epicgetter(args, ver)
    invstart(args, ver)
    time.sleep(invtime)
    invstop(args, ver)
    delete(args, ver)
    modeposter(args, off, ver)