# This test posts an SSL key and certificate from the key and cert files in this testing framework. User must ensure path and file contents are correct.
# This test also checks invalid ssl credentials do not work


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

key = open(r'***', "rb").read()
cert = open(r'***', "rb").read()

keyjunk = "asdfjkl;qweruiopzxcv.,mni-" * 62
certjunk = "zxcv;lkjqwer" * 89

params = {"Good Cert and Key":(202, key, cert),
"Bad Contents Good Header":(400, "{}{}{}".format(key[0:32], keyjunk[:-9], key[-31:]), "{}{}{}".format(cert[0:28], certjunk[:-9], cert[-27:])),
"Random Cert and Key":(400, keyjunk, certjunk),
"Missing a Character":(400, key[1:], cert[1:])}

certloaded = False
keyloaded = False

def reboot(args):
    print("Performing reboot ...")
    try:
        response = requests.post(
             "{}/***/v0/reader/boot".format(sec),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=18
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
             timeout=args["timeout"])
        print(response.json())
    except Exception as exc:
        print("Exception {}".format(exc))

def getter(args, ver):
    response = requests.get(
         "{}/***/v0/ssl/".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},verify=ver
         )
    response_body = response.json()
    print(response_body, response.status_code)
    check.equal(response_body['certificate']['loaded'], True, "Certificate AND key should be loaded if this function is run")
    check.equal(response_body['key']['loaded'], True, "Certificate AND key should be loaded if this function is run")
    
def delete(args, ver):
    response =  requests.delete("{}/***/v0/ssl/".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, verify=ver)
    print(response.status_code, "delete")

def keyposter(payload, message, err , args, ver):
    response = requests.post(
         "{}/***/v0/ssl/key".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, data=payload, verify=ver
         )
    print(response.status_code, "key post")
    check.equal(response.status_code, err, "did not post key correctly \n {}".format(message))
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(args, ver)
    else:
        check.equal(response.status_code, err, "did not post cert correctly \n {}".format(message))

def certposter(payload, message, err ,args, ver):
    response = requests.post(
         "{}/***/v0/ssl/cert".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, data=payload, verify=ver
         )
    print(response.status_code, "cert post")
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        keyposter(key, message, err, args, ver)
    else:
        check.equal(response.status_code, err, "did not post cert correctly \n {}".format(message))

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        key = y[1]
        cert = y[2]
        print(message)         
        certposter(cert, message, err, args, ver)
        delete(args, ver)
        getter(args, ver)
    #reboot(args)        
    test_count += 1
    return test_count

def test_ssl(ip, serial, tout, do_reset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    unpacker(params, args, ver)

    