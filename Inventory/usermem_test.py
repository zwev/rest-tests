# For this test to work the memory of at least one tag MUST be set to "0A0B0C0D0E0F".
# This test looks for any tags with a PC of 3400, and stores whatever data the reader sees based on "Start" and "Length" values supplied.
# The data retrieved is then checked against the expected data.


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

hexdata = ["0A0B0C0D0E0F", "0C0D0E0F", "0A0B0C0D"]
params = {"Three words": (0, 0, 3, 0),
"Last Two words": (0, 1, 2, 1),
"First Two words": (0, 0, 2, 2),
}

def getter(args, message, ant, start, length, idx, ver):
    try:
        response = requests.get(
            "{}/***/v0/inv/rdbank?antenna_id={}&access_pwd={}&bank={}&start={}&length={}".format(sec, ant, 00000000, 3, start, length),
            headers={"Authorization": "Bearer " + args['serial']}, timeout=args['timeout'], verify=ver, stream=False
            )
        print(response.status_code)
        tag_data = []
        data_tags = 0
        response_body = response.json()
        for item in response_body:
            if item['pc'] == '3400':
                tag_data.append(item['data'])
                data_tags += 1
        print("{} tags with data encoded".format(data_tags))
        print(tag_data)
        if len(tag_data) == 0:
            check.greater_equal(len(tag_data), 1, "No encoded tags seen")
        else:
            check.is_in(hexdata[idx], tag_data, message)
    except:
        print("Error reading from data bank")


def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        ant = y[0]
        start = y[1] 
        length = y[2]
        idx = y[3]      
        getter(args, message, ant, start, length, idx, ver)
        time.sleep(3)
        test_count += 1
    return test_count

def test_readmem(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    unpacker(params, args, ver)