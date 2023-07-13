# This test posts specific settings to the reader as well as a valid EPIC key.
# After posting and verifying that the settings are correct, an inventory is run and read rates are checked to be within the expected range for sensitive mode.

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

select_settings = {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}
RF_settings = {'rfmode': '1',}
invtime = 10
filter = {"bank": 1, "start": 32, "length": 32, "mask": "0x15C62536"}
on = {
"mode": 0,
"enabled": True
}
off = {
"mode": 0,
"enabled": False
}
epic = False

def filterposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    print(response.status_code, payload)

def filtergetter(args,payload, ver):
    response = requests.get(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(json.dumps(response_body, indent=2))
    check.equal(payload, response_body)

def selposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args["timeout"], verify=ver
         )
    print(response.status_code)

def RFposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    print(response.status_code)



def RFgetter(args, payload, ver):
    response = requests.get(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)


def deletefilter(args, ver):
    response = requests.delete(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )


def selgetter(args, payload, ver):
    response = requests.get(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def epicgetter(args, ver):
    response = requests.get(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(json.dumps(response_body, indent=2))
    if response_body['enabled'] == True:
        global epic 
        epic = True
    else:
        epic = False

def keyposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/epic/key".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, data=payload, timeout=args["timeout"], verify=ver
         )
    print(response.status_code)

def modeposter(args, payload, ver):
    response = requests.post(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args["timeout"], verify=ver
         )
    print(response.status_code)

def invstart(args, ver):
    response = requests.get(
         "{}/***/v0/inv/start".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()


def invstop(args, ver):
    response = requests.get(
         "{}/***/v0/inv/stop".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    tags = {}
    total_reads = 0
    if epic == True:
        for item in response_body:
            total_reads += sum(item["count"])
            if item["pc"] not in tags:
                tags[item["pc"]] = []
            if item["epc"] not in tags[item["pc"]]:
                tags[item["pc"]].append(item["epc"])
        print(json.dumps(tags, indent=2))
        check.is_not_in("4155", tags.keys(), "Epic Tags Should be Decoded")
        tags.clear()
    else:
        for item in response_body:
            total_reads += sum(item["count"])
            if item["pc"] not in tags:
                tags[item["pc"]] = []
            if item["epc"] not in tags[item["pc"]]:
                tags[item["pc"]].append(item["epc"])
        print(json.dumps(tags, indent=2))
        print("{} reads per second".format(total_reads/invtime))
        check.is_in("4155", tags.keys())
        check.less_equal(total_reads/invtime, 200, "200 max")
        check.greater_equal(total_reads/invtime, 100, "100 min")
        tags.clear()

def delete(args, ver):
    response = requests.delete("{}/***/v0/epic/key".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver)
    print(response.status_code)




def test_epicsens(ip, serial, tout, do_reset, ssl, ver):
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
    filterposter(args, filter, ver)
    filtergetter(args, filter, ver)
    epicgetter(args, ver)
    invstart(args, ver)
    time.sleep(invtime)
    invstop(args, ver)
    delete(args, ver)
    deletefilter(args, ver)
    modeposter(args, off, ver)

