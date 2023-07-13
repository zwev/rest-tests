# This test posts various antenna powers at each possible antenna to the reader and checks that invalid power/antenna configs do not post.
#  It also checks that returned power/antenna config are what was posted.

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
    "All Good 0;5;5": (0, 202, {"read_power": "5.00", "write_power": "5.00"}), 
    "All Good 1;5;5": (1, 202, {"read_power": "5.00", "write_power": "5.00"}), 
    "All Good 2;5;5": (2, 202, {"read_power": "5.00", "write_power": "5.00"}), 
    "All Good 3;5;5": (3, 202, {"read_power": "5.00", "write_power": "5.00"}),
    "All Good 0;33;33": (0, 202, {"read_power": "33.00", "write_power": "33.00"}), 
    "All Good 1;33;33": (1, 202, {"read_power": "33.00", "write_power": "33.00"}), 
    "All Good 2;33;33": (2, 202, {"read_power": "33.00", "write_power": "33.00"}), 
    "All Good 3;33;33": (3, 202, {"read_power": "33.00", "write_power": "33.00"}),
    "All Good 0;15;15": (0, 202, {"read_power": "15.00", "write_power": "15.00"}), 
    "All Good 1;15;15": (1, 202, {"read_power": "15.00", "write_power": "15.00"}), 
    "All Good 2;15;15": (2, 202, {"read_power": "15.00", "write_power": "15.00"}), 
    "All Good 3;15;15": (3, 202, {"read_power": "15.00", "write_power": "15.00"}),
    "Read 0;Int;15": (0, 202, {"read_power": 15.00, "write_power": "15.00"}), 
    "Read 1;Int;15": (1, 202, {"read_power": 15.00, "write_power": "15.00"}), 
    "Read 2;Int;15": (2, 202, {"read_power": 15.00, "write_power": "15.00"}), 
    "Read 3;Int;15": (3, 202, {"read_power": 15.00, "write_power": "15.00"}),
    "Write 0;Int;15": (0, 202, {"read_power": "15.00", "write_power": 15.00}), 
    "Write 1;Int;15": (1, 202, {"read_power": "15.00", "write_power": 15.00}), 
    "Write 2;Int;15": (2, 202, {"read_power": "15.00", "write_power": 15.00}), 
    "Write 3;Int;15": (3, 202, {"read_power": "15.00", "write_power": 15.00}),

    "Bad Powers 0;0;0": (0, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Powers 1;0;0": (1, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Powers 2;0;0": (2, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Powers 3;0;0": (3, 404, {"read_power": "0.00", "write_power": "0.00"}),
    "Bad Powers 0;4.5;4.5": (0, 404, {"read_power": "4.50", "write_power": "4.50"}), 
    "Bad Powers 1;4.5;4.5": (1, 404, {"read_power": "4.50", "write_power": "4.50"}), 
    "Bad Powers 2;4.5;4.5": (2, 404, {"read_power": "4.50", "write_power": "4.50"}), 
    "Bad Powers 3;4.5;4.5": (3, 404, {"read_power": "4.50", "write_power": "4.50"}),
    "Bad Powers 0;33.5;33.5": (0, 404, {"read_power": "33.50", "write_power": "33.50"}), 
    "Bad Powers 1;33.5;33.5": (1, 404, {"read_power": "33.50", "write_power": "33.50"}), 
    "Bad Powers 2;33.5;33.5": (2, 404, {"read_power": "33.50", "write_power": "33.50"}), 
    "Bad Powers 3;33.5;33.5": (3, 404, {"read_power": "33.50", "write_power": "33.50"}),
    "Bad Powers 0;50;50": (0, 404, {"read_power": "50.00", "write_power": "50.00"}), 
    "Bad Powers 1;50;50": (1, 404, {"read_power": "50.00", "write_power": "50.00"}), 
    "Bad Powers 2;50;50": (2, 404, {"read_power": "50.00", "write_power": "50.00"}), 
    "Bad Powers 3;50;50": (3, 404, {"read_power": "50.00", "write_power": "50.00"}),

    "Bad Read 0;0;15": (0, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Read 1;0;15": (1, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Read 2;0;15": (2, 404, {"read_power": "0.00", "write_power": "0.00"}), 
    "Bad Read 3;0;15": (3, 404, {"read_power": "0.00", "write_power": "0.00"}),
    "Bad Read 0;45;15": (0, 404, {"read_power": "45.00", "write_power": "15.00"}), 
    "Bad Read 1;45;15": (1, 404, {"read_power": "45.00", "write_power": "15.00"}), 
    "Bad Read 2;45;15": (2, 404, {"read_power": "45.00", "write_power": "15.00"}), 
    "Bad Read 3;45;15": (3, 404, {"read_power": "45.00", "write_power": "15.00"}),
    "Bad Read 0;Str;15": (0, 404, {"read_power": "FAIL", "write_power": "0.00"}), 
    "Bad Read 1;Str;15": (1, 404, {"read_power": "FAIL", "write_power": "0.00"}), 
    "Bad Read 2;Str;15": (2, 404, {"read_power": "FAIL", "write_power": "0.00"}), 
    "Bad Read 3;Str;15": (3, 404, {"read_power": "FAIL", "write_power": "0.00"}),
    "Bad Read 0;Int;15": (0, 404, {"read_power": 50.00, "write_power": "15.00"}), 
    "Bad Read 1;Int;15": (1, 404, {"read_power": 50.00, "write_power": "15.00"}), 
    "Bad Read 2;Int;15": (2, 404, {"read_power": 50.00, "write_power": "15.00"}), 
    "Bad Read 3;Int;15": (3, 404, {"read_power": 50.00, "write_power": "15.00"}),
    "Bad Read 0;Bool;15": (0, 404, {"read_power": True, "write_power": "0.00"}), 
    "Bad Read 1;Bool;15": (1, 404, {"read_power": True, "write_power": "0.00"}), 
    "Bad Read 2;Bool;15": (2, 404, {"read_power": True, "write_power": "0.00"}), 
    "Bad Read 3;Bool;15": (3, 404, {"read_power": True, "write_power": "0.00"}),
    "Bad Read 0;Empty;15": (0, 404, {"read_power": "", "write_power": "15"}), 
    "Bad Read 1;Empty;15": (1, 404, {"read_power": "", "write_power": "15"}), 
    "Bad Read 2;Empty;15": (2, 404, {"read_power": "", "write_power": "15"}), 
    "Bad Read 3;Empty;15": (3, 404, {"read_power": "", "write_power": "15"}),
    "Bad Read 0;500000000;15": (0, 404, {"read_power": "500000000", "write_power": "15"}), 
    "Bad Read 1;500000000;15": (1, 404, {"read_power": "500000000", "write_power": "15"}), 
    "Bad Read 2;500000000;15": (2, 404, {"read_power": "500000000", "write_power": "15"}), 
    "Bad Read 3;500000000;15": (3, 404, {"read_power": "500000000", "write_power": "15"}),
    
    "Bad Write 0;33.5;0": (0, 404, {"read_power": "33.50", "write_power": "0"}), 
    "Bad Write 1;33.5;0": (1, 404, {"read_power": "33.50", "write_power": "0"}), 
    "Bad Write 2;33.5;0": (2, 404, {"read_power": "33.50", "write_power": "0"}), 
    "Bad Write 3;33.5;0": (3, 404, {"read_power": "33.50", "write_power": "0"}),
    "Bad Write 0;15;50": (0, 404, {"read_power": "15", "write_power": "50.00"}), 
    "Bad Write 1;15;50": (1, 404, {"read_power": "15", "write_power": "50.00"}), 
    "Bad Write 2;15;50": (2, 404, {"read_power": "15", "write_power": "50.00"}), 
    "Bad Write 3;15;50": (3, 404, {"read_power": "15", "write_power": "50.00"}),
    "Bad Write 0;33.5;Str": (0, 404, {"read_power": "33.50", "write_power": "FAIL"}), 
    "Bad Write 1;33.5;Str": (1, 404, {"read_power": "33.50", "write_power": "FAIL"}), 
    "Bad Write 2;33.5;Str": (2, 404, {"read_power": "33.50", "write_power": "FAIL"}), 
    "Bad Write 3;33.5;Str": (3, 404, {"read_power": "33.50", "write_power": "FAIL"}),
    "Bad Write 0;15;Int": (0, 404, {"read_power": "15", "write_power": 50.00}), 
    "Bad Write 1;15;Int": (1, 404, {"read_power": "15", "write_power": 50.00}), 
    "Bad Write 2;15;Int": (2, 404, {"read_power": "15", "write_power": 50.00}), 
    "Bad Write 3;15;Int": (3, 404, {"read_power": "15", "write_power": 50.00}),
    "Bad Write 0;33.5;Bool": (0, 404, {"read_power": "33.50", "write_power": True}), 
    "Bad Write 1;33.5;Bool": (1, 404, {"read_power": "33.50", "write_power": True}), 
    "Bad Write 2;33.5;Bool": (2, 404, {"read_power": "33.50", "write_power": True}), 
    "Bad Write 3;33.5;Bool": (3, 404, {"read_power": "33.50", "write_power": True}),
    "Bad Write 0;15;Empty": (0, 404, {"read_power": "15", "write_power": ""}), 
    "Bad Write 1;15;Empty": (1, 404, {"read_power": "15", "write_power": ""}), 
    "Bad Write 2;15;Empty": (2, 404, {"read_power": "15", "write_power": ""}), 
    "Bad Write 3;15;Empty": (3, 404, {"read_power": "15", "write_power": ""}),
    "Bad Write 0;15;500000000": (0, 404, {"read_power": "15", "write_power": "500000000"}), 
    "Bad Write 1;15;500000000": (1, 404, {"read_power": "15", "write_power": "500000000"}), 
    "Bad Write 2;15;500000000": (2, 404, {"read_power": "15", "write_power": "500000000"}), 
    "Bad Write 3;15;500000000": (3, 404, {"read_power": "15", "write_power": "500000000"}),

    "valid ant 0 Bad Data Str": (0, 404, {"read_power": "FAIL", "write_power": "FAIL"}), 
    "valid ant 1 Bad Data Int": (1, 404, {"read_power": 50.00, "write_power": 50.00}), 
    "valid ant 2 Bad Data Bool": (2, 404, {"read_power": True, "write_power": False}), 
    "valid ant 3 Bad Data Empty": (3, 404, {"read_power": "", "write_power": ""}),
    "valid ant 3 Bad Data 500000000": (3, 404, {"read_power": "500000000", "write_power": "500000000"}),


    "ant ID out of bounds valid power": (4, 404, {"read_power": "5.00", "write_power": "5.00"}),
    "ant ID out of bounds valid power 2": (-1, 404, {"read_power": "5.00", "write_power": "5.00"}),
    "ant ID out of bounds power too low": (4, 404, {"read_power": "0.00", "write_power": "0.00"}),
    "ant ID out of bounds power too high": (-1, 404, {"read_power": "50.00", "write_power": "50.00"}),
    "bad json 0": (0, 400, {"rad_power": "5", "write_power": "5"}),
    "bad json 1": (1, 400, {"read_power": "5", "stuff": "10", "write_power": "5"}),
    "bad json 2": (2, 400, {"read_power": "5", "rite_power": "5"}),
    "bad json 3": (3, 400, {}),
    }


def poster(message, id, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/ant/pwr/{}".format(sec, id),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args["timeout"], verify=ver
         )
    
    print(message, "==>", payload)
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message, id, payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def getter(message, id, payload, args, ver):
    response = requests.get(
         "{}/***/v0/ant/pwr/{}".format(sec, id),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    #print(json.dumps(response_body, indent=2))
    payload2 = {k:float(v) for k,v in payload.items()}
    response_body2 = {k:float(v) for k,v in response_body.items()}
    check.equal(payload2, response_body2, message)
    
def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        id = y[0]
        err = y[1]
        payload = y[2]         
        poster(message, id, err, payload, args, ver)
        test_count += 1
    return test_count


def test_power(ip, serial, tout, do_reset, ssl, ver):
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

#getter("test", 0, {"read_power": "5.00", "write_power": "5.00"} )
        

