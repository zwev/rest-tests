# This test uses RegEx patterns to check that the data returned for the reader info API call is within certain boundries.
# These patterns should work for future builds, versions, and serial numbers for all *** readers but can be easilly changed if needed.

from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check

import sys
import pytest
import time
import re

sys.path.append('..')
from common.shared import factory_reset, ssl_reset

models = ["SO21330","SP13350", "SE24370"]
buildpattern =  r"^B\.2[0-9]\.[01][0-9]\.[0-3][0-9]\.[05][0-9]$"
serialpattern = r"^[0-9]{2}[A-Z0-9][0-9]{5}$"
versionpattern = r"^V[0-9]\.[0-9]\.[0-9]"
bootpattern = r"^V[0-9]\.[0-9]"

def getter(args, ver):
    test_count = 0
    response = requests.get(
         "{}/***/v0/reader".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    x = response_body["model"]
    modelmatch = lambda x: True if x in models else False
    serialmatch = re.match(serialpattern, response_body["serial_no"])
    buildmatch = re.match(buildpattern, response_body["build_no"])
    versionmatch = re.match(versionpattern, response_body["version"])
    bootmatch = re.match(bootpattern, response_body["bootloader"])
    matchlist = {"model": modelmatch(x),"serial": bool(serialmatch),"build": bool(buildmatch),"version": bool(versionmatch),"boot": bool(bootmatch)}
    print(matchlist)
    for x, y in matchlist.items():
        check.is_true(y)
        test_count += 1
    print("")
    print("Ran ", test_count, " tests")


def unpacker(args, ver):
    getter(args, ver)


def test_info(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    print("")
    unpacker(args, ver)
    print("")
