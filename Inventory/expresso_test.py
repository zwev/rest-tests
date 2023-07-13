# This test posts specific settings to the reader and verifies that settings are correct.
# Then an inventory is run and read rates are checked to be within the expected range for Expresso mode.
# Because the test is being run in Expresso mode, A tag pop is supplied that cooresponds to the full, half, and quarter of the inventory time in milliseconds.

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

params = {"2000 Tag Pop": ({'rfmode': '4', "est_tag_pop": "5000"}, 500, 700),
"1000 Tag Pop": ({'rfmode': '4', "est_tag_pop": "2500"}, 200, 500),
"250 Tag Pop": ({'rfmode': '4', "est_tag_pop": "1250"}, 100, 200),}

select_settings = {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'A','sel_flag': 'All'}
invtime = 5
dwell = {"dwell_time": "5000"}

def dwellposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/ant/dwell".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    print(response.status_code)

def dwellgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/ant/dwell".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    check.equal(payload, response_body)

def selposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, json=payload, timeout=args["timeout"], verify=ver
         )
    print(response.status_code)
    
def RFposter(payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    print(response.status_code)

def RFgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)

def selgetter(payload, args, ver):
    response = requests.get(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response_body)


def epcgetter(args, ver):
    response = requests.get(
         "{}/***/v0/inv/start".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2), response.status_code)
    #check.equal(payload, response_body, message)

def invstop(args, high, low, ver):
    response = requests.get(
         "{}/***/v0/inv/stop".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    count = 0
    for item in response_body:
        print(item["count"])
        for x in item["count"]:
            count += x
    print("{} tag reads per second".format(count/invtime))
    check.less_equal(count/invtime, high, "Too High")
    check.greater_equal(count/invtime, low, "Too Low")

def timed(args, ver):
    response = requests.get(
         "{}/***/v0/inv/timed".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver,
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

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        rf = y[0]
        low = y[1]
        high = y[2]
        RFposter(rf, args, ver)
        RFgetter(rf, args, ver)
        epcgetter(args, ver)
        time.sleep(invtime)
        invstop(args, high, low, ver)
        #timed(args, ver)          
        test_count += 1

    return test_count

def test_expresso(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    selposter(select_settings, args, ver)
    selgetter(select_settings, args, ver)
    dwellposter(dwell, args, ver)
    dwellgetter(dwell, args, ver)
    unpacker(params, args, ver)
    