# This test posts non-default settings to the reader, resets the reader, then checks that settings have been reverted to default.


from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check

import sys
import pytest
import time

from conftest import ver

sys.path.append('..')
from common.shared import factory_reset, ssl_reset

default = None

params = {"Non-Default Settings": (202, {
  "antenna_setup": {
    "sequence": [
      0,1,0,1
    ],
    "dwell_time": {"dwell_time": "550"},      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "15.00",
        "write_power": "15.00"
      },
      {
        "antenna_id": "1",
        "read_power": "15.00",
        "write_power": "15.00"
      },
      {
        "antenna_id": "2",
        "read_power": "15.00",
        "write_power": "15.00"
      },
      {
        "antenna_id": "3",
        "read_power": "15.00",
        "write_power": "15.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "3"
    },
    "q_algorithm": {
      "algo_type": "static",
      "start_q": 3
    },
    "select_control": {
      "select_session": "S0",
      "query_session": "S0",
      "select_action": "101",
      "query_target": "A",
      "sel_flag": "SL"
    },
    "advanced": {
      "drm_active": False,
      "select_setup": {
        "mode": 2,
        "preselect_count": 2,
        },
        "hopping_interval": 400
    }
  }
}),}

non_default_url = [("POST", "{}/***/v0/ant/dwell", params["Non-Default Settings"][1]["antenna_setup"]["dwell_time"]),
("POST", "{}/***/v0/ant/pwr", params["Non-Default Settings"][1]["antenna_setup"]["power_levels"]), 
("POST", "{}/***/v0/ant/seq", params["Non-Default Settings"][1]["antenna_setup"]["sequence"]),
("POST", "{}/***/v0/rain/adv", params["Non-Default Settings"][1]["rain"]["advanced"]),
("POST", "{}/***/v0/rain/qalg", params["Non-Default Settings"][1]["rain"]["q_algorithm"]),
("POST", "{}/***/v0/rain/rfmode", params["Non-Default Settings"][1]["rain"]["rfmode"]),
("POST", "{}/***/v0/rain/sel", params["Non-Default Settings"][1]["rain"]["select_control"])]

default_url = None

def saver(args, ver):
    print("Save")
    try:
        response = requests.post(
             "{}/***/v0/reader/save".format(sec),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=args["timeout"], verify=ver
             )
        print("Response: ", response.status_code)
    except:
        print("Caught timeout. Proceeding to verify command actually did its job.")
    """
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message,payload, args)
    else:
        check.equal(err, response.status_code, message)"""
    print("Done")

def restorer(args, ver):
    print("Restore")
    try:
        response = requests.post(
            "{}/***/v0/reader/restore".format(sec),
            headers={"Authorization": "Bearer " + args["serial"]},
            timeout=args["timeout"], verify=ver
            )
        print("Response: ", response.status_code)
    except:
        print("Caught timeout. Proceeding to verify command actually did its job.")
    #print(json.dumps(response_body, indent=2))
    print("Done")

def reboot(args, ver):
    print("Performing reboot ...")
    try:
        response = requests.post(
             "{}/***/v0/reader/boot".format(sec),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=18, verify=ver
             )
        print("Response:", response.status_code)
    except Exception as exc:
        print("Factory reset raised exception {}".format(exc))

    print("Waiting for reboot to complete")
    time.sleep(15)
    print("Testing connectivity: ", end='')
    try:
        response = requests.get("{}/***/v0/reader/name".format(sec),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=args["timeout"], verify=ver)
        print(response.json())
    except Exception as exc:
        print("Exception {}".format(exc))

def run_request(method, url, message, err, payload, args, ver):
    response = requests.request(
        method,
        url.format(sec),
        headers={"Authorization": "Bearer " + args["serial"]},
        json=payload,
        timeout=args["timeout"], verify=ver
        )
    if method == "GET":
        check.equal(payload, response.json())
        if url[:-3] == "sel":
            payload2 = {k.upper():v.upper() for k,v in payload.items()}
            response_body2 = {k.upper():v.upper() for k,v in response.json().items()}
            check.equal(payload2, response_body2, "Select settings did not save properly")
    if method == "POST":
        print(message, "==>", payload)
        if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
            run_request("GET", url, message, err, payload, args, ver)
        else:
            check.equal(err, response.status_code, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        #payload = y[1] Referance Not Needed
        for x in non_default_url:
            method = x[0]
            url = x[1]
            data = x[2]
            run_request(method, url, message, err, data, args, ver)
        factory_reset(args)
        for x in default_url:
            method = "GET"
            url = x[1]
            data = x[2]
            run_request(method, url, message, err, data, args, ver)
        test_count += 1
    return test_count


def test_saverestore(ip, serial, tout, do_reset, defaultset, ssl, ver):
    global default
    global default_url
    default = defaultset

    default_url = [("POST", "{}/***/v0/ant/dwell", default["antenna_setup"]["dwell_time"]),
    ("POST", "{}/***/v0/ant/pwr", default["antenna_setup"]["power_levels"]), 
    ("POST", "{}/***/v0/ant/seq", default["antenna_setup"]["sequence"]),
    ("POST", "{}/***/v0/rain/adv", default["rain"]["advanced"]),
    ("POST", "{}/***/v0/rain/qalg", default["rain"]["q_algorithm"]),
    ("POST", "{}/***/v0/rain/rfmode", default["rain"]["rfmode"]),
    ("POST", "{}/***/v0/rain/sel", default["rain"]["select_control"])]

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