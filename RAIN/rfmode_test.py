# This test checks that each RF mode, as well as various tag populations for expresso mode can be correctly posted to the reader.
# Also checks that invalid RF modes/data do not post and that returned data is what was posted.

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

    
    "Good 0": (202, {'rfmode': '0',}),
    "Good Sensitive": (202, {'rfmode': '1',}),
    "Good Other": (202, {'rfmode': '2',}),
    "Good Fast": (202, {'rfmode': '3',}),
    
    "Expresso 150": (202, {'rfmode': '4', 'est_tag_pop': '150'}),
    "Expresso 200": (202, {'rfmode': '4', 'est_tag_pop': '200'}),
    "Expresso 300": (202, {'rfmode': '4', 'est_tag_pop': '300'}),
    "Expresso 450": (202, {'rfmode': '4', 'est_tag_pop': '450'}),
    "Expresso 600": (202, {'rfmode': '4', 'est_tag_pop': '600'}),
    "Expresso 900": (202, {'rfmode': '4', 'est_tag_pop': '900'}),
    "Expresso 2200": (202, {'rfmode': '4', 'est_tag_pop': '2200'}),
    "Expresso INT 2200": (202, {'rfmode': 4, 'est_tag_pop': 2200}),

    "Expresso 1": (404, {'rfmode': '4', 'est_tag_pop': '1'}),
    "Expresso 0": (404, {'rfmode': '4', 'est_tag_pop': '0'}),
    "Expresso -1": (404, {'rfmode': '4', 'est_tag_pop': '-1'}),
    "Expresso Missing": (404, {'rfmode': '4',}),

    "0 W/ Tags": (202, {'rfmode': '0',}),
    "Sensitive W/ Tags": (404, {'rfmode': '1', 'est_tag_pop': '150'}),
    "Other W/ Tags": (404, {'rfmode': '2', 'est_tag_pop': '150'}),
    "Fast W/ Tags": (404, {'rfmode': '3', 'est_tag_pop': '150'}),

    "Bad RF": (404, {'rfmode': '99', 'est_tag_pop': '300'}),

    "Bad JSON 1": (400, {'rfmode': '1', 'est_tag_pop': '300', "Extra": "Data"}),
    "Bad JSON 2": (400, {'': '1', 'est_tag_pop': '300'}),
    "Bad JSON 3": (400, {}),
    "Bad JSON 4": (400, {'rtfmode ': '1', 'est_tag_pop': '300'}),
    "Bad JSON 5": (404, {'est_tag_pop': '300'}),
    
}

def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/rfmode".format(sec),
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
         "{}/***/v0/rain/rfmode".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    if message == "Expresso INT 2200":
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


def test_rf(ip, serial, tout, do_reset, ssl, ver):
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

#test()

