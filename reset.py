from pytest_check.check_methods import check_func
import requests
import json
from requests.models import Response
import pytest_check as check

ip = "***"
serial = "***"


def poster():
    response = requests.post(
         "http://{}/***/v0/reader/cfg/factory".format(ip),
         headers={"Authorization": "Bearer " + serial},
         )
    print(response.status_code)
poster()