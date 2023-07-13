# This test posts valid Q algorithm settings to the reader and checks that invalid settings do not post.
# It also checks that returned settings is what was posted.

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

params = {

    "Good Dynamic 3.0.5": (202, {'algo_type': 'dynamic', 'start_q': 3, 'min_q': 0, 'max_q': 5}),
    "Good Dynamic 6.3.8": (202, {'algo_type': 'dynamic', 'start_q': 6, 'min_q': 3, 'max_q': 8}),
    "Good Dynamic 9.6.11": (202, {'algo_type': 'dynamic', 'start_q': 9, 'min_q': 6, 'max_q': 11}),
    "Good Dynamic 12.9.15": (202, {'algo_type': 'dynamic', 'start_q': 12, 'min_q': 9, 'max_q': 15}),
    "Good Dynamic 15.15.15": (202, {'algo_type': 'dynamic', 'start_q': 15, 'min_q': 15, 'max_q': 15}),
    "Good Dynamic 0.0.0": (202, {'algo_type': 'dynamic', 'start_q': 0, 'min_q': 0, 'max_q': 0}),
    "Good Dynamic STR 0.0.0": (202, {'algo_type': 'dynamic', 'start_q': "0", 'min_q': "0", 'max_q': "0"}),


    "Good Static 0": (202, {'algo_type': 'static', 'start_q': 0, }),
    "Good Static 3": (202, {'algo_type': 'static', 'start_q': 3, }),
    "Good Static 6": (202, {'algo_type': 'static', 'start_q': 6, }),
    "Good Static 9": (202, {'algo_type': 'static', 'start_q': 9, }),
    "Good Static 12": (202, {'algo_type': 'static', 'start_q': 12, }),
    "Good Static 15": (202, {'algo_type': 'static', 'start_q': 15,}),
    "Good Static STR 15": (202, {'algo_type': 'static', 'start_q': "15",}),


    "Bad Data type 1": (404, {'algo_type': 'super dynamic', 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad Data type 2": (404, {'algo_type': True, 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad Data type 3": (404, {'algo_type': '', 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad Data type 4": (404, {'algo_type': 2, 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad json 1": (400, {'': 'dynamic', 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad json 2": (400, {'algo_type': 'dynamic', "extra": "data", 'start_q': 0, 'min_q': 0, 'max_q': 15}),
    "Bad Json 3": (400, {'': 'static', 'start_q': 10,}),
    "Bad Json 4": (400, {'algo_type': 'static', 'extra': 'data', 'start_q': 10,}),
    "Bad Dynamic 50.3.15": (404, {'algo_type': 'dynamic', 'start_q': 50, 'min_q': 3, 'max_q': 15}),
    "Bad Dynamic 5.3.16": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': 3, 'max_q': 16}),
    "Bad Dynamic 5.-1.15": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': -1, 'max_q': 15}),
    "Bad Dynamic A.3.15": (404, {'algo_type': 'dynamic', 'start_q': 'a', 'min_q': 3, 'max_q': 15}),
    "Bad Dynamic 5.B.15": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': 'b', 'max_q': 15}),
    "Bad Dynamic 5.3.C": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': 3, 'max_q': 'c'}),
    "Bad Dynamic Bool.3.15": (404, {'algo_type': 'dynamic', 'start_q': True, 'min_q': 3, 'max_q': 15}),
    "Bad Dynamic 5.Bool.15": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': True, 'max_q': 15}),
    "Bad Dynamic 5.3.Bool": (404, {'algo_type': 'dynamic', 'start_q': 5, 'min_q': 3, 'max_q': True}),
    "Bad Dynamic M.0.5": (404, {'algo_type': 'dynamic', 'min_q': 0, 'max_q': 5}),
    "Bad Dynamic 6.M.8": (404, {'algo_type': 'dynamic', 'start_q': 6, 'max_q': 8}),
    "Bad Dynamic 9.6.M": (404, {'algo_type': 'dynamic', 'start_q': 9, 'min_q': 6,}),
    "Bad Dynamic 0.3.15": (404, {'algo_type': 'dynamic', 'start_q': 0, 'min_q': 3, 'max_q': 15}),
    "Bad Static 50": (404, {'algo_type': 'static', 'start_q': 50,}),
    "Bad Static -10": (404, {'algo_type': 'static', 'start_q': -10,}),
    "Bad Static M": (404, {'algo_type': 'static', }),
    }

def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/qalg".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args['timeout'], verify=ver
         )
    
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message,payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def getter(message, payload, args, ver):
    response = requests.get(
         "{}/***/v0/rain/qalg".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    if message == "Good Dynamic STR 0.0.0" or "Good Static STR 15":
        payload.pop('algo_type')
        response_body.pop('algo_type')
        payload2 = {k:float(v) for k,v in payload.items()}
        response_body2 = {k:float(v) for k,v in response_body.items()}
        check.equal(payload2, response_body2, message)
    else:
        check.equal(payload, response_body, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]         
        poster(message, err, payload, args, ver)
        test_count += 1
    return test_count


def test_qsettings(ip, serial, tout, do_reset, ssl, ver):
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