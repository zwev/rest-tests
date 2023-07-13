# This test posts various valid filter settings to the reader and verifies that invalid filter settings will not post.
# It also checks that posted settings are indeed what is returned via a GET.

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

params = {"good filter" : (202, {"bank": 1, "start": 32, "length": 32, "mask": "0xE2004202"}),
"non-matching filter" : (202, {"bank": 1, "start": 32, "length": 32, "mask": "0xE2808254"}),
"Bad Bank 1" : (404, {"bank": 10, "start": 32, "length": 32, "mask": "0xE2004202"}),
"Bad Bank 2" : (404, {"bank": -1, "start": 32, "length": 32, "mask": "0xE2004202"}),
"Bad Bank 3" : (404, {"bank": True, "start": 32, "length": 32, "mask": "0xE2004202"}),
"Bad Bank 4" : (404, {"bank": "1", "start": 32, "length": 32, "mask": "0xE2004202"}),
"Bad Start 1" : (404, {"bank": 1, "start": True, "length": 32, "mask": "0xE2004202"}),
"Bad Start 2" : (404, {"bank": 1, "start": "32", "length": 32, "mask": "0xE2004202"}),
"Bad Start 3" : (404, {"bank": 1, "start": -1, "length": 32, "mask": "0xE2004202"}),
"Bad Start 4" : (404, {"bank": 1, "start": 999, "length": 32, "mask": "0xE2004202"}),
"Bad Length 1" : (404, {"bank": 1, "start": 32, "length": False, "mask": "0xE2004202"}),
"Bad Length 2" : (404, {"bank": 1, "start": 32, "length": "32", "mask": "0xE2004202"}),
"Bad Length 3" : (404, {"bank": 1, "start": 32, "length": -1, "mask": "0xE2004202"}),
"Bad Length 4" : (404, {"bank": 1, "start": 32, "length": 999, "mask": "0xE2004202"}),
"Bad Mask 1" : (404, {"bank": "1", "start": 32, "length": 32, "mask": 3}),
"Bad Mask 2" : (404, {"bank": 1, "start": 32, "length": 32, "mask": True}),
"Bad Mask 3" : (404, {"bank": 1, "start": 32, "length": 32, "mask": "Bad Mask"}),
"Bad Mask 4" : (404, {"bank": 1, "start": 32, "length": 32, "mask": -1}),

"bad Json" : (400, {"start": 32, "length": 32, "mask": 3}),
}

def filterposter(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        filtergetter(message,payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def filtergetter(message, payload, args, ver):
    response = requests.get(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    check.equal(payload, response_body, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]         
        filterposter(message, err, payload, args, ver)
        deletefilter(args, ver)
        test_count += 1
    return test_count
    
def deletefilter(args, ver):
    response = requests.delete(
         "{}/***/v0/inv/filter".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )


def test_filter(ip, serial, tout, do_reset, ssl, ver):
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



