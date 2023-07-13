# This test posts various dwell times to the reader and checks that invalid dwell times do not post. It also checks that returned dwll times are the posted dwell time.
# Additionally, this test is slightly different from the other Antenna and RAIN tests; it uses the run_request function for the get and post request.
# If needed all other tests can relatively easily be modified to run in a similar fashion.

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
    "dwell 50": (202, {"dwell_time": "50"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 100": (202, {"dwell_time": "100"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 150": (202, {"dwell_time": "150"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 200": (202, {"dwell_time": "200"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 250": (202, {"dwell_time": "250"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 300": (202, {"dwell_time": "300"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 350": (202, {"dwell_time": "350"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 400": (202, {"dwell_time": "400"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 450": (202, {"dwell_time": "450"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 500": (202, {"dwell_time": "500"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 550": (202, {"dwell_time": "550"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 600": (202, {"dwell_time": "600"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 650": (202, {"dwell_time": "650"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 700": (202, {"dwell_time": "700"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 750": (202, {"dwell_time": "750"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 800": (202, {"dwell_time": "800"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 850": (202, {"dwell_time": "850"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 900": (202, {"dwell_time": "900"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 950": (202, {"dwell_time": "950"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 1000": (202, {"dwell_time": "1000"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell int": (202, {"dwell_time": 1000}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 5000000000": (404, {"dwell_time": "5000000000"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 72.5531": (404, {"dwell_time": "72.5531"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 49": (404, {"dwell_time": "49"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 10": (404, {"dwell_time": "10"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell 0": (404, {"dwell_time": "0"}, "{}/***/v0/ant/dwell", "POST"),
    "dwell -1": (404, {"dwell_time": "-1"}, "{}/***/v0/ant/dwell", "POST"),
    "Invald data bool": (404, {"dwell_time": True}, "{}/***/v0/ant/dwell", "POST"),
    "Invalid data string": (404, {"dwell_time": "Plz 400"}, "{}/***/v0/ant/dwell", "POST"),
    "Invalid data empty": (404, {"dwell_time": ""}, "{}/***/v0/ant/dwell", "POST"),
    "Bad Json": (400, {"": "50"}, "{}/***/v0/ant/dwell", "POST"),
    #should cases where time is left out be treated as a 404 as in bad json 2?
    "Bad Json 2": (400, {"dwell_tme": "50"}, "{}/***/v0/ant/dwell", "POST"),
    "Bad Json 3": (400, {}, "{}/***/v0/ant/dwell", "POST"),
    "Bad Json 4": (400, {"dwell_time": "50", "bad": "data"}, "{}/***/v0/ant/dwell", "POST"),
    }

def run_request(method, url, message, err, payload, ver, args):
    response = requests.request(
        method,
        url.format(sec),
        headers={"Authorization": "Bearer " + args["serial"]},
        json=payload,
        timeout=args["timeout"], verify=ver
        )
    if method == "GET":
        if message == "dwell int":
            payload2 = {k:float(v) for k, v in response.json().items()}
            response2 = {k:float(v) for k, v in response.json().items()}
            check.equal(payload2, response2, message)
        else:
            check.equal(payload, response.json(), message)
    if method == "POST":
        print(message, "==>", payload)
        if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
            run_request("GET", url, message, err, payload, ver, args)
        else:
            check.equal(err, response.status_code, message)

def unpacker(params, ver, args):
    test_count = 0

    for message, stuff in params.items():
        err = stuff[0] 
        payload = stuff[1]
        url = stuff[2]
        method = stuff[3]
        run_request(method, url, message, err, payload, ver, args)
        test_count += 1

    return test_count

def test_dwell(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    print("")
    test_count = unpacker(params, ver, args)
    print("")
    print("Ran ", test_count, " tests")

