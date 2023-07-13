# This test posts various antenna powers at each possible antenna to the reader and checks that invalid power/antenna configs do not post.
# It also checks that returned power/antenna config are what was posted.
# Unlike power_test.py this tests the api call to set all antenna power levels.

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

sec = "http://"

params = {
    "All Good 5;5": (202, [
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "All Good 33;33": (202, [
        {"antenna_id": "0", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "1", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "2", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "3", "read_power": "33.00", "write_power": "33.00"},
        ]), 
    "All Good 15;15": (202, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "15.00"},
        ]),
    " Good Read int 15;15": (202, [
        {"antenna_id": "0", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "1", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "2", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "3", "read_power": 15.00, "write_power": "15.00"},
        ]),
    " Good Power int 15;15": (202, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": 15.00},
        {"antenna_id": "1", "read_power": "15.00", "write_power": 15.00},
        {"antenna_id": "2", "read_power": "15.00", "write_power": 15.00},
        {"antenna_id": "3", "read_power": "15.00", "write_power": 15.00},
        ]),
    "Good AntID int 15;15": (202, [
        {"antenna_id": 0, "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": 1, "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": 2, "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": 3, "read_power": "15.00", "write_power": "15.00"},
        ]),
    "Bad Power 50;50": (404, [
        {"antenna_id": "0", "read_power": "50.00", "write_power": "50.00"},
        {"antenna_id": "1", "read_power": "50.00", "write_power": "50.00"},
        {"antenna_id": "2", "read_power": "50.00", "write_power": "50.00"},
        {"antenna_id": "3", "read_power": "50.00", "write_power": "50.00"},
        ]),
    "Bad Power 33.5;33.5": (404, [
        {"antenna_id": "0", "read_power": "33.50", "write_power": "33.50"},
        {"antenna_id": "1", "read_power": "33.50", "write_power": "33.50"},
        {"antenna_id": "2", "read_power": "33.50", "write_power": "33.50"},
        {"antenna_id": "3", "read_power": "33.50", "write_power": "33.50"},
        ]),
    "Bad Power 0;0": (404, [
        {"antenna_id": "0", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "1", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "2", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "3", "read_power": "0.00", "write_power": "0.00"},
        ]),
    "Bad Power 15;0": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": "0.00"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "0.00"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "0.00"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "0.00"},
        ]),
    "Bad Power 15;50": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": "50.00"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "50.00"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "50.00"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "50.00"},
        ]),
    "Bad Power 33.5;15": (404, [
        {"antenna_id": "0", "read_power": "33.50", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "33.50", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "33.50", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "33.50", "write_power": "15.00"},
        ]),
    "Bad Power 4.5;15": (404, [
        {"antenna_id": "0", "read_power": "4.50", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "4.50", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "4.50", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "4.50", "write_power": "15.00"},
        ]),
    "Bad Power 4.5;4.5": (404, [
        {"antenna_id": "0", "read_power": "4.50", "write_power": "4.50"},
        {"antenna_id": "1", "read_power": "4.50", "write_power": "4.50"},
        {"antenna_id": "2", "read_power": "4.50", "write_power": "4.50"},
        {"antenna_id": "3", "read_power": "4.50", "write_power": "4.50"},
        ]),
    "Bad Power Str;15": (404, [
        {"antenna_id": "0", "read_power": "FAIL", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "FAIL", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "FAIL", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "FAIL", "write_power": "15.00"},
        ]),
    "Bad Power Int;15": (202, [
        {"antenna_id": "0", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "1", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "2", "read_power": 15.00, "write_power": "15.00"},
        {"antenna_id": "3", "read_power": 15.00, "write_power": "15.00"},
        ]),
    "Bad Power Bool;15": (404, [
        {"antenna_id": "0", "read_power": True, "write_power": "15.00"},
        {"antenna_id": "1", "read_power": True, "write_power": "15.00"},
        {"antenna_id": "2", "read_power": True, "write_power": "15.00"},
        {"antenna_id": "3", "read_power": True, "write_power": "15.00"},
        ]),
    "Bad Power Empty;15": (404, [
        {"antenna_id": "0", "read_power": "", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "", "write_power": "15.00"},
        ]),
    "Bad Power 500000000;15": (404, [
        {"antenna_id": "0", "read_power": "500000000", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "500000000", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "500000000", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "500000000", "write_power": "15.00"},
        ]),
    "Bad Power 15;Str": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": "FAIL"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "FAIL"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "FAIL"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "FAIL"},
        ]),
    "Bad Power 15;Bool": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": True},
        {"antenna_id": "1", "read_power": "15.00", "write_power": True},
        {"antenna_id": "2", "read_power": "15.00", "write_power": True},
        {"antenna_id": "3", "read_power": "15.00", "write_power": True},
        ]),
    "Bad Power 15;Empty": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": ""},
        {"antenna_id": "1", "read_power": "15.00", "write_power": ""},
        {"antenna_id": "2", "read_power": "15.00", "write_power": ""},
        {"antenna_id": "3", "read_power": "15.00", "write_power": ""},
        ]),
    "Bad Power 15;500000000": (404, [
        {"antenna_id": "0", "read_power": "15.00", "write_power": "500000000"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "500000000"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "500000000"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "500000000"},
        ]),
    "Bad power Ant OOB1 0;0": (404, [
        {"antenna_id": "0", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "1", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "2", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "4", "read_power": "0.00", "write_power": "0.00"},
        ]),
    "Bad Power Ant OOB2 15;15": (404, [
        {"antenna_id": "-1", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "1", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "2", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "3", "read_power": "15.00", "write_power": "15.00"},
        ]),
        "Bad Power Ant OOB3 0;0": (404, [
        {"antenna_id": "0", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "1", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "6", "read_power": "0.00", "write_power": "0.00"},
        {"antenna_id": "3", "read_power": "0.00", "write_power": "0.00"},
        ]),
    "Bad Power Ant OOB4 15;15": (404, [
        {"antenna_id": "4", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "5", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "6", "read_power": "15.00", "write_power": "15.00"},
        {"antenna_id": "7", "read_power": "15.00", "write_power": "15.00"},
        ]),
    "Missing Field0 5;5": (202, [
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Missing Field1 5;5": (202, [
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Missing Field2 5;5": (202, [
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Missing Field3 5;5": (202, [
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "bad json body 1": (400,[
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3","rad_power": "5.00", "write_power": "5.00"},
        ]),
    "bad json body 2": (400,[
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "rite_power": "5.00"},
        {"antenna_id": "3","read_power": "5.00", "write_power": "5.00"},
        ]),
    "bad json body 3": (400,[
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3","read_power": "5.00", "write_power": "5.00"},
        ]),
    "bad json body 4": (400,[
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3","junk": 99, "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Fields Out of Order0 5;5": (202, [
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},        
        ]),
    "Fields Out of Order1 5;5": (202, [
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Fields Out of Order2 5;5": (202, [
        {"antenna_id": "2", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "3", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "0", "read_power": "5.00", "write_power": "5.00"},
        {"antenna_id": "1", "read_power": "5.00", "write_power": "5.00"},
        ]),
    "Reset power": (202, [
        {"antenna_id": "0", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "1", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "2", "read_power": "33.00", "write_power": "33.00"},
        {"antenna_id": "3", "read_power": "33.00", "write_power": "33.00"},
        ]),

    }

def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/ant/pwr".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message,payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def getter(message, payload, args, ver):
    response = requests.get(
         "{}/***/v0/ant/pwr".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    payload2 = {k:float(v) for k,v in payload[0].items()}
    response_body2 = {k:float(v) for k,v in response_body[0].items()}
    check.equal(payload2, response_body2, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]         
        poster(message, err, payload, args, ver)
        test_count += 1
    return test_count


def test_allpower(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    print("")
    test_count = unpacker(params, args, ver)
    print("")
    print("Ran ", test_count, " tests")


