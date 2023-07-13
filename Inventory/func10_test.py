# This test posts specific settings to the reader and verifys that the settings are correct
# Afterwards, an inventory is run and read rates are checked to be within the expected range.

from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check

import sys
import pytest
import time

sys.path.append('..')
from common.shared import factory_reset, ssl_reset

seq = [0,1]
select_settings = {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}
RF_settings = {'rfmode': '1',}
invtime = 10

def seqposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/ant/seq".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args['timeout'], verify=ver
         )
    print(response.status_code)

def seqgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/ant/seq".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    check.equal(payload, response_body)

def selposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args['timeout'], verify=ver
         )
    print(response.status_code)
    
def RFposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args['timeout'], verify=ver
         )
    print(response.status_code)

def RFgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def selgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)


def epcgetter(args, ver):
    response = requests.get(
         "{}/***/v0/inv/start".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2), response.status_code)
    #check.equal(payload, response_body, message)

def invstop(args, ver):
    response = requests.get(
         "{}/***/v0/inv/stop".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2), response.status_code)
    count = 0
    for item in response_body:
        print(item["count"])
        for x in item["count"]:
            count += x
    print("{} tag reads per second".format(count/invtime))
    check.less_equal(count/invtime, 200, "200 max")
    check.greater_equal(count/invtime, 130, "130 min")

def timed(args, ver):
    response = requests.get(
         "{}/***/v0/inv/timed".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2), response.status_code)
    count = 0
    for item in response_body:
        print(item["count"])
        for x in item["count"]:
            count += x
    print("{} tag reads per second".format(count/invtime))
    check.less_equal(count/invtime, 200, "200 max")
    check.greater_equal(count/invtime, 130, "130 min")

def test_func10(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    selposter(select_settings, args, ver)
    RFposter(RF_settings, args, ver)
    seqposter(seq, args, ver)
    seqgetter(seq, args, ver)
    selgetter(select_settings, args, ver)
    RFgetter(RF_settings, args, ver)
    epcgetter(args, ver)
    time.sleep(invtime)
    invstop(args, ver)
    timed(args, ver)
