# This contains a factory reset function that is referenced throughout every test.

from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check
import pytest
import time

def factory_reset(args):
    print("Performing factory reset ...")
    try:
        response = requests.post(
             "http://{}/***/v0/reader/factory".format(args['ip']),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=5
             )
        print("Response:", response.status_code)
    except Exception as exc:
        print("Factory reset raised exception {}".format(exc))

    print("Waiting for reboot to complete")
    time.sleep(15)
    print("Testing connectivity: ", end='')
    try:
        response = requests.get("http://{}/***/v0/reader/name".format(args['ip']),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=args["timeout"])
        print(response.json())
    except Exception as exc:
        print("Exception {}".format(exc))

def ssl_reset(args, ssl, ver):
    print("Performing factory reset for SSL testing...")
    try:
        response = requests.post(
             "https://{}/***/v0/reader/factory".format(args['ip']),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=5, verify=ver
             )
        print("Response:", response.status_code)
    except Exception as exc:
        print("Factory reset raised exception {}".format(exc))

    print("Waiting for reboot to complete")
    time.sleep(15)
    print("Testing connectivity: ", end='')
    try:
        response = requests.get("http://{}/***/v0/reader/name".format(args['ip']),
             headers={"Authorization": "Bearer " + args["serial"]},
             timeout=args["timeout"])
        print(response.json())
    except Exception as exc:
        print("Exception {}".format(exc))
    print("Posting SSL cert and key...")
    time.sleep(15)
    keyposter(args, ssl, ver)
    certposter(args, ssl, ver)
    getter(args, ssl, ver)


def keyposter(args, ssl, ver):
    sec = "http{}://{}".format(str(ssl), args['ip'])
    payload = open(r'***', "rb")
    response = requests.post(
         "{}/***/v0/ssl/key".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, data=payload, verify=ver
         )
    print(response.status_code)

def certposter(args, ssl, ver):
    sec = "http{}://{}".format(str(ssl), args['ip'])
    payload = open(r'***', "rb")
    response = requests.post(
         "{}/***/v0/ssl/cert".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, data=payload, verify=ver
         )
    print(response.status_code)

def getter(args, ssl, ver):
    sec = "http{}://{}".format(str(ssl), args['ip'])
    response = requests.get(
         "{}/***/v0/ssl/".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]}, verify=ver
         )
    response_body = response.json()
    print(response_body, response.status_code)
