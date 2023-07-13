# This test posts various valid/invalid epic configs to the reader and checks that invalid configs do not post.
# It also checks that returned epic config is what was posted.

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

keys = {
    "Good Key": (202, """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}),
    "Bad Key 1": (404, """*** Customer Profile
Customer SU811255; Codec SC0001
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (title)": (404, """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (Cust Id)": (404, """*** Customer Profile
Customer SU811275; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (Codec)": (404, """*** Customer Profile
Customer SU811255; Codec SC0008
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (line 1)": (404, """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA69
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (line 2)": (404, """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531A29BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BBCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}), 
    "Bad Key (line 3)": (404, """*** Customer Profile
Customer SU811255; Codec SC0001
508625363ECB6E62455082158E26BBB7367AC0C01D6608CB66E709BF777B7EA6
B24BB21531829BFD5902204F6A3284A87F76D353CC6C5016B7F849E2EB698FBC
BCE0D53A32304AB8012A322326DB944621765E59CE1716C8C7E2F44513AA251""", 
{
  "mode": 0,
  "enabled": False,
  "customer_id": "SU811255",
  "codec": "SC0001"
}),
}

good_test_modes = {
    "Good Mode 1 (Good Key)": (202, {"mode": 0,"enabled": True}, {"mode": 0,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 2 (Good Key)": (202, {"mode": 0,"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 3 (Good Key)": (202, {"mode": 1,"enabled": True}, {"mode": 1,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 4 (Good Key)": (202, {"mode": 1,"enabled": False}, {"mode": 1,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 5 (Good Key)": (202, {"mode": 6,"enabled": True}, {"mode": 6,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 6 (Good Key)": (202, {"mode": 6,"enabled": False}, {"mode": 6,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 7 (Good Key)": (202, {"mode": 7,"enabled": True}, {"mode": 7,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
    "Good Mode 8 (Good Key)": (202, {"mode": 7,"enabled": False}, {"mode": 7,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Bad Type 1 (Good Key)": (404, {"mode": 0,"enabled": 'no'}, {}),
    "Bad Type 2 (Good Key)": (404, {"mode": 0,"enabled": 4}, {}),
    "Bad Mode 1 (Good Key)": (404, {"mode": -1,"enabled": True}, {}),
    "Bad Mode 2 (Good Key)": (404, {"mode": -1,"enabled": False}, {}),
    "Bad Mode 3 (Good Key)": (404, {"mode": 8,"enabled": True}, {}),
    "Bad Mode 4 (Good Key)": (404, {"mode": 8,"enabled": False}, {}),
    "Bad JSON 1 (Good Key)": (400, {"mod": 8,"enabled": False}, {}),
    "Bad JSON 2 (Good Key)": (404, {"mode": "Ughhh","enabled": False}, {}),
    "Bad JSON 3 (Good Key)": (400, {"mode": 8,"enabledx": False}, {}),
    "Bad JSON 4 (Good Key)": (404, {"mode": 8,"enabled": 0}, {}),
    "Bad JSON 5 (Good Key)": (404, {"mode": 8,"enabled": "False"}, {}),
    "Bad JSON 6 (Good Key)": (400, "", {}),
    "Bad JSON 7 (Good Key)": (400, "This is not JSON", {}),
    "Reset status (Good Key)": (202, {"mode": 0,"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Optional Field 1 (Good Key)": (202, {"enabled": True}, {"mode": 0,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
    "Optional Field 2 (Good Key)": (202, {"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    #enabled status for next 2 tests depends on immediately proceeding test.
    "Optional Field 3 (Good Key)": (202, {"mode": 1}, {"mode": 1,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Optional Field 4 (Good Key)": (202, {"mode": 0}, {"mode": 0,"enabled": False,"customer_id": "SU811255","codec": "SC0001"}),
    "Optional Field 5 (Good Key)": (400, {}, {}),
    "Reset status 2 (Good Key)": (202, {"mode": 0,"enabled": True}, {"mode": 0,"enabled": True,"customer_id": "SU811255","codec": "SC0001"}),
}

bad_test_modes = {
    "Good Mode 1 (Bad Key)": (404, {"mode": 0,"enabled": True}, {}),
    "Good Mode 2 (Bad Key)": (202, {"mode": 0,"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Good Mode 3 (Bad Key)": (404, {"mode": 1,"enabled": True}, {}),
    "Good Mode 4 (Bad Key)": (202, {"mode": 1,"enabled": False}, {"mode": 1,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Good Mode 5 (Bad Key)": (404, {"mode": 6,"enabled": True}, {}),
    "Good Mode 6 (Bad Key)": (202, {"mode": 6,"enabled": False}, {"mode": 6,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Good Mode 7 (Bad Key)": (404, {"mode": 7,"enabled": True}, {}),
    "Good Mode 8 (Bad Key)": (202, {"mode": 7,"enabled": False}, {"mode": 7,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Bad Type 1 (Bad Key)": (404, {"mode": 0,"enabled": 'no'}, {}),
    "Bad Type 2 (Bad Key)": (404, {"mode": 0,"enabled": 4}, {}),
    "Bad Mode 1 (Bad Key)": (404, {"mode": -1,"enabled": True}, {}),
    "Bad Mode 2 (Bad Key)": (404, {"mode": -1,"enabled": False}, {}),
    "Bad Mode 3 (Bad Key)": (404, {"mode": 8,"enabled": True}, {}),
    "Bad Mode 4 (Bad Key)": (404, {"mode": 8,"enabled": False}, {}),
    "Bad JSON 1 (Bad Key)": (400, {"modex": 8,"enabled": False}, {}),
    "Bad JSON 2 (Bad Key)": (404, {"mode": "Ughhh","enabled": False}, {}),
    "Bad JSON 3 (Bad Key)": (400, {"mode": 8,"enable": False}, {}),
    "Bad JSON 4 (Bad Key)": (404, {"mode": 8,"enabled": 0}, {}),
    "Bad JSON 5 (Bad Key)": (404, {"mode": 8,"enabled": "False"}, {}),
    "Reset status (Bad Key)": (202, {"mode": 0,"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Optional Field 1 (Bad Key)": (404, {"enabled": True}, {}),
    "Optional Field 2 (Bad Key)": (202, {"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}),
    #enabled status for next test depends on immediately proceeding test.
    "Optional Field 3 (Bad Key)": (202, {"mode": 1}, {"mode": 1,"enabled": False,"customer_id": "        ","codec": "      "}),
    "Optional Field 4 (Bad Key)": (400, {}, {}),
    "Reset status 2 (Good Key)": (202, {"mode": 0,"enabled": False}, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}),
}


def getter(message, payload, args, ver):
    response = requests.get(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )

    #print(json.dumps(payload, indent=2))
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    check.equal(payload['customer_id'], response_body['customer_id'], message)
    check.equal(payload['mode'], response_body['mode'], message)

def modegetter(message, expected_response_body, args, ver):
    response = requests.get(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )

    #print(json.dumps(expected_response_body, indent=2))
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    check.equal(expected_response_body, response_body, message)

def poster(message, err, key, payload, args, ver):
    response = requests.post(
        "{}/***/v0/epic/key".format(sec),
        headers={"Authorization": "Bearer " + args["serial"]},
        data=key,
        timeout=args["timeout"], verify=ver
        )

    print(message, "==>", payload)
    #print(message, "---", response.status_code)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message, payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def modeposter(message, err, payload, expected_response_body, args, ver):
    response = requests.post(
         "{}/***/v0/epic".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )

    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        modegetter(message, expected_response_body, args, ver)
    else:
        check.equal(err, response.status_code, message)
    

def delete(message, args, ver):
    response = requests.delete("{}/***/v0/epic/key".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, verify=ver)
    print(message, "==> delete response:", response.status_code)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        key = y[1] 
        payload = y[2]      
        poster(message, err, key, payload, args, ver)
        time.sleep(.05)
        delete(message, args, ver)
        test_count += 1
    return test_count

def mode_unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]
        expected_response_body = y[2]
        modeposter(message, err, payload, expected_response_body, args, ver)
        time.sleep(.05)
        test_count += 1
    return test_count


def test_epic(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)

    print("")
    print("Testing setting of EPIC Customer Keys")
    key_test_count = unpacker(keys, args, ver)

    print("")
    print("Testing setting mode and enable status for Good EPIC Customer Key")
    good_epic_key = "Good Key"
    poster(good_epic_key, keys[good_epic_key][0], keys[good_epic_key][1], keys[good_epic_key][2], args, ver)
    mode_test_count = mode_unpacker(good_test_modes, args, ver)
    delete(good_epic_key, args, ver)

    # While we're here, let's make sure the correct response is returned after deleting a good customer key
    print("")
    print("Verifying response to GET status after good key has been deleted")
    modegetter(good_epic_key, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}, args, ver)

    print("")
    print("Testing setting mode and enable status for Bad EPIC Customer Key")
    bad_epic_key = "Bad Key 1"
    poster(bad_epic_key, keys[bad_epic_key][0] ,keys[bad_epic_key][1], keys[bad_epic_key][2], args, ver)
    mode_test_count += mode_unpacker(bad_test_modes, args, ver)

    # While we're here, let's check response after trying to install bad key and running different POST status commands
    print("")
    print("Verifying response to GET status after bad key has been 'installed'")
    modegetter(bad_epic_key, {"mode": 0,"enabled": False,"customer_id": "        ","codec": "      "}, args, ver)

    delete(bad_epic_key, args, ver)

    print("")
    print("Ran ", key_test_count + mode_test_count, " tests")
