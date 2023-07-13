# This test posts various antenna sequence data to the reader and checks that invalid sequence data do not post.
# It also checks that returned sequence is what was posted.

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
    "Good SEQ0": (202, [0]),
    "Good SEQ1": (202, [1]),
    "Good SEQ2": (202, [2]),
    "Good SEQ3": (202, [3]),
    "Good SEQ4": (202, [0, 1]),
    "Good SEQ5": (202, [0, 2]),
    "Good SEQ6": (202, [0, 1, 2]),
    "Good SEQ7": (202, [0, 1, 2, 3]),
    "Good SEQ8": (202, [3, 2, 1, 0]),
    "Good SEQ9": (202, [1, 1, 1, 1, 1, 1, 1, 1]),
    "Good SEQ STR":(202, ["0"]),
    "Invalid SEQ1": (400, []),
    "Invalid SEQ2": (404, [4]),
    "Invalid SEQ3": (404, [-1]),
    "Invalid SEQ4": (404, [0, 1, 2, 3, 4]),
    "Invalid SEQ5": (404, [0, 1, 2, 3, 4]),
    "Invalid SEQ6": (400, [1, 1, 1, 1, 1, 1, 1, 1, 1]),
    "Reset Seq": (202, [0]),
    }

def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/ant/seq".format(sec),
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
         "{}/***/v0/ant/seq".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    payload2 = {float(v) for v in payload}
    response_body2 = {float(v) for v in response_body}
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


def test_sequence(ip, serial, tout, do_reset, ssl, ver):
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

