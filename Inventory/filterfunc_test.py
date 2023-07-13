# This test posts specific settings to the reader in order to filter a set of known tags in the field. for this test to work, tags MUST be encoded with the correct EPC's.
# After posting and verifying that the settings are correct, an inventory is run and the returned tags are checked to make sure they match the supplied filter. 
# Filter is then deleted and the test continues with the next mask in the same way.

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

test_list = [(0, 0, "A"), (0, 0, "B"), (1, 1, "A"), (1, 2, "B"), (2, 2, "A"), (2, 1, "B")]

masklist = ["", "0xE2004202", "0x15C62536"]
masklist_compare = [x[2::] for x in masklist]
mask_template = {"bank": 1, "start": 32, "length": 32, "mask": ""}

invtime = 10
select_settings = {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}
antenna_sequence = [0]
rf_settings = {'rfmode': '1'}

settings = [("POST", "{}/***/v0/ant/seq", antenna_sequence),
            ("POST", "{}/***/v0/rain/rfmode", rf_settings)]

def run_request(method, url, payload, args, ver):
    response = requests.request(
        method,
        url.format(sec),
        headers={"Authorization": "Bearer " + args["serial"]},
        json=payload,
        timeout=args["timeout"], verify=ver
        )
    getter(url, payload, args, ver)

def getter(url, payload, args, ver):
    response = requests.get(
         url.format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args["timeout"], verify=ver
         )
    response_body = response.json()
    print(response_body)
    check.equal(payload, response.json())

def epcgetter(args, ver):
    response = requests.get(
         "{}/***/v0/inv/start".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()

def invstop(args, ver, mask=""):
    response = requests.get(
         "{}/***/v0/inv/stop".format(sec),
         headers={"Authorization": "Bearer " + args['serial']}, timeout=args["timeout"], verify=ver
         )
    response_body = response.json()

    if mask != "":
        print("Inventory run with: {} applied as mask".format(mask))
    else: 
        print("No Mask Applied")

    epc_list= list(filter(lambda x: x["epc"][0:8] in masklist_compare, response_body))
    for item in epc_list:
        print(item["epc"])

    mask_list = [mask[2::] for item in epc_list]

    if mask != "":
        truncated_epcs = [item["epc"][0:8] for item in epc_list]
        check.equal(mask_list, truncated_epcs, "EPCs all matched mask")


def unpacker(params, args, ver):
    test_count = 0

    for method, url, setting in settings:
        run_request(method, url, setting, args, ver)

    for maskidx, maskjdx, target in params:
        mask_template["mask"] = masklist[maskidx]
        if masklist[maskidx] == "":
            mask_template["length"] = 0
        else:
            mask_template["length"] = 32

        select_settings["query_target"] = target
        run_request("POST", "{}/***/v0/inv/filter", mask_template, args, ver)
        run_request("POST", "{}/***/v0/rain/sel", select_settings, args, ver)

        epcgetter(args, ver)
        time.sleep(invtime)
        invstop(args, ver, mask=masklist[maskjdx])                         
        test_count += 1

    # Clear the filter and compare to the template with length = 0 & mask = ""
    mask_template["mask"] = ""
    mask_template["length"] = 0
    run_request("DELETE", "{}/***/v0/inv/filter", mask_template, args, ver)
    return test_count


def test_filterfunc(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    print("")
    test_count = unpacker(test_list, args, ver)
    print("")
    print("Ran ", test_count, " tests")