# This test posts an antenna sequence to the reader and based on the message the unpacker function will change the authentication sent to the reader with the post.


from pytest_check.check_methods import check_func
import requests
import json
from requests.models import HTTPBasicAuth, Response
import pytest_check as check

import sys
import pytest
import time

sys.path.append('..')
from common.shared import factory_reset, ssl_reset


params = {
    "Good Token": (202, [0],),
    "Typo Token": (401, [0]),
    "Empty Token": (401, [0]),
    "User Pass Token": (202, [0],"Bearer"),
    }

def bearerposter(message, err, payload, args, token, ver):
    response = requests.post(
         "{}/***/v0/ant/seq".format(sec),
         headers={"Authorization": "Bearer " + token},
         json=payload,
         timeout=args['timeout'], verify=ver
         )
    
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message,payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def userpassposter(message, err, payload, args, token, user, ver):
    response = requests.post(
         "{}/***/v0/ant/seq".format(sec),
         auth=HTTPBasicAuth('{}'.format(user), '{}'.format(token)),
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
         "{}/***/v0/ant/seq".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
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
        if message == "Good Token" or "User Pass Token":
            token = args["serial"]
        if message == "Typo Token":
            token = args["serial"][1::]
        if message == "Empty Token":
            token = ""
        bearerposter(message, err, payload, args, token, ver)
        if len(y) == 3:
            user = y[2]
            token = args["serial"]
            userpassposter(message,err,payload, args, token, user, ver)
        test_count += 1

    return test_count


def test_auth(ip, serial, tout, do_reset, ssl, ver):
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
