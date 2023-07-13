# This test posts almost every possible valid select setting combination to the reader and checks that invalid sequence data do not post.
# It also checks that returned sequence is what was posted.
# The various good select settings all test for "All" being set to select flag; different select flags are tested after the bulk of these good combinations.

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


params = {
    
    "Select Good 00.1D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.1A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.1B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 00.2D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.2A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.2B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '001','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.3D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.3A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.3B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '010','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.4D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.4A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.4B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '011','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.5D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.5A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.5B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '100','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.6D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.6A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.6B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '101','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.7D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.7A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.7B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '110','query_target': 'B','sel_flag': 'All'}),

    "Select Good 00.8D": (202, {'select_session': 'S0','query_session': 'S0','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 00.8A": (202, {'select_session': 'S0','query_session': 'S0','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 00.8B": (202, {'select_session': 'S0','query_session': 'S0','select_action': '111','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 01.1D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.1A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.1B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 01.2D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.2A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.2B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '001','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.3D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.3A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.3B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '010','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.4D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.4A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.4B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '011','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.5D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.5A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.5B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '100','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.6D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.6A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.6B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '101','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.7D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.7A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.7B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '110','query_target': 'B','sel_flag': 'All'}),

    "Select Good 01.8D": (202, {'select_session': 'S0','query_session': 'S1','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 01.8A": (202, {'select_session': 'S0','query_session': 'S1','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 01.8B": (202, {'select_session': 'S0','query_session': 'S1','select_action': '111','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 02.1D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.1A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.1B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '000','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 02.2D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.2A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.2B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.3D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.3A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.3B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.4D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.4A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.4B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.5D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.5A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.5B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.6D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.6A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.6B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.7D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.7A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.7B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 02.8D": (202, {'select_session': 'S0','query_session': 'S2','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 02.8A": (202, {'select_session': 'S0','query_session': 'S2','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 02.8B": (202, {'select_session': 'S0','query_session': 'S2','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 03.1D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.1A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.1B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '000','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 03.2D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.2A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.2B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.3D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.3A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.3B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.4D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.4A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.4B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.5D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.5A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.5B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.6D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.6A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.6B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.7D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.7A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.7B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 03.8D": (202, {'select_session': 'S0','query_session': 'S3','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 03.8A": (202, {'select_session': 'S0','query_session': 'S3','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 03.8B": (202, {'select_session': 'S0','query_session': 'S3','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 10.1D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.1A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.1B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '000','query_target': 'B','sel_flag': 'All'}),

    "Select Good 10.2D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.2A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.2B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.3D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.3A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.3B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.4D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.4A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.4B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.5D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.5A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.5B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.6D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.6A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.6B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.7D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.7A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.7B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 10.8D": (202, {'select_session': 'S1','query_session': 'S0','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 10.8A": (202, {'select_session': 'S1','query_session': 'S0','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 10.8B": (202, {'select_session': 'S1','query_session': 'S0','select_action': '111','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 11.1D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.1A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.1B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good 11.2D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.2A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.2B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.3D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.3A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.3B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.4D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.4A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.4B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.5D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.5A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.5B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.6D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.6A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.6B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.7D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.7A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.7B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 11.8D": (202, {'select_session': 'S1','query_session': 'S1','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 11.8A": (202, {'select_session': 'S1','query_session': 'S1','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 11.8B": (202, {'select_session': 'S1','query_session': 'S1','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 12.1D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.1A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.1B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 12.2D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.2A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.2B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.3D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.3A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.3B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.4D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.4A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.4B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.5D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.5A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.5B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.6D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.6A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.6B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.7D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.7A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.7B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 12.8D": (202, {'select_session': 'S1','query_session': 'S2','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 12.8A": (202, {'select_session': 'S1','query_session': 'S2','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 12.8B": (202, {'select_session': 'S1','query_session': 'S2','select_action': '111','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.1D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.1A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.1B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 13.2D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.2A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.2B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.3D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.3A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.3B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.4D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.4A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.4B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.5D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.5A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.5B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.6D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.6A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.6B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.7D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.7A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.7B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 13.8D": (202, {'select_session': 'S1','query_session': 'S3','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 13.8A": (202, {'select_session': 'S1','query_session': 'S3','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 13.8B": (202, {'select_session': 'S1','query_session': 'S3','select_action': '111','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.1D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.1A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.1B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 20.2D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.2A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.2B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.3D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.3A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.3B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.4D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.4A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.4B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.5D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.5A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.5B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.6D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.6A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.6B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.7D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.7A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.7B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 20.8D": (202, {'select_session': 'S2','query_session': 'S0','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 20.8A": (202, {'select_session': 'S2','query_session': 'S0','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 20.8B": (202, {'select_session': 'S2','query_session': 'S0','select_action': '111','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.1D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.1A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.1B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 21.2D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.2A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.2B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.3D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.3A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.3B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.4D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.4A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.4B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.5D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.5A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.5B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.6D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.6A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.6B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.7D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.7A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.7B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 21.8D": (202, {'select_session': 'S2','query_session': 'S1','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 21.8A": (202, {'select_session': 'S2','query_session': 'S1','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 21.8B": (202, {'select_session': 'S2','query_session': 'S1','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 22.1D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.1A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.1B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 22.2D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.2A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.2B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.3D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.3A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.3B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.4D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.4A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.4B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.5D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.5A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.5B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.6D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.6A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.6B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.7D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.7A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.7B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 22.8D": (202, {'select_session': 'S2','query_session': 'S2','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 22.8A": (202, {'select_session': 'S2','query_session': 'S2','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 22.8B": (202, {'select_session': 'S2','query_session': 'S2','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 23.1D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.1A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.1B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 23.2D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.2A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.2B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.3D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.3A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.3B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.4D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.4A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.4B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.5D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.5A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.5B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.6D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.6A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.6B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.7D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.7A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.7B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 23.8D": (202, {'select_session': 'S2','query_session': 'S3','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 23.8A": (202, {'select_session': 'S2','query_session': 'S3','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 23.8B": (202, {'select_session': 'S2','query_session': 'S3','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 30.1D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.1A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.1B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 30.2D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.2A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.2B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.3D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.3A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.3B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.4D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.4A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.4B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.5D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.5A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.5B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.6D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.6A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.6B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.7D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.7A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.7B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 30.8D": (202, {'select_session': 'S3','query_session': 'S0','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 30.8A": (202, {'select_session': 'S3','query_session': 'S0','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 30.8B": (202, {'select_session': 'S3','query_session': 'S0','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 31.1D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.1A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.1B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 31.2D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.2A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.2B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.3D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.3A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.3B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.4D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.4A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.4B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.5D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.5A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.5B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.6D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.6A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.6B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.7D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.7A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.7B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 31.8D": (202, {'select_session': 'S3','query_session': 'S1','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 31.8A": (202, {'select_session': 'S3','query_session': 'S1','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 31.8B": (202, {'select_session': 'S3','query_session': 'S1','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 32.1D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.1A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.1B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 32.2D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.2A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.2B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.3D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.3A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.3B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.4D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.4A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.4B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.5D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.5A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.5B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.6D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.6A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.6B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.7D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.7A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.7B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 32.8D": (202, {'select_session': 'S3','query_session': 'S2','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 32.8A": (202, {'select_session': 'S3','query_session': 'S2','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 32.8B": (202, {'select_session': 'S3','query_session': 'S2','select_action': '111','query_target': 'B','sel_flag': 'All'}),

    "Select Good 33.1D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.1A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '000','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.1B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '000','query_target': 'B','sel_flag': 'All'}),
   
    "Select Good 33.2D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '001','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.2A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '001','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.2B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '001','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.3D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '010','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.3A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '010','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.3B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '010','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.4D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '011','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.4A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '011','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.4B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '011','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.5D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '100','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.5A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '100','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.5B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '100','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.6D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '101','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.6A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '101','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.6B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '101','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.7D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '110','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.7A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '110','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.7B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '110','query_target': 'B','sel_flag': 'All'}),
 
    "Select Good 33.8D": (202, {'select_session': 'S3','query_session': 'S3','select_action': '111','query_target': 'Dual','sel_flag': 'All'}),
    "Select Good 33.8A": (202, {'select_session': 'S3','query_session': 'S3','select_action': '111','query_target': 'A','sel_flag': 'All'}),
    "Select Good 33.8B": (202, {'select_session': 'S3','query_session': 'S3','select_action': '111','query_target': 'B','sel_flag': 'All'}),
    
    "Select Good S0 ~SL": (202, {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': '~SL'}),
    "Select Good S0 SL": (202, {'select_session': 'S0','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'SL'}),
    "Select Good S1 ~SL": (202, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': '~SL'}),
    "Select Good S1 SL": (202, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'SL'}),
    "Select Good S2 ~SL": (202, {'select_session': 'S2','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': '~SL'}),
    "Select Good S2 SL": (202, {'select_session': 'S2','query_session': 'S2','select_action': '000','query_target': 'Dual','sel_flag': 'SL'}),
    "Select Good S3 ~SL": (202, {'select_session': 'S3','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': '~SL'}),
    "Select Good S3 SL": (202, {'select_session': 'S3','query_session': 'S3','select_action': '000','query_target': 'Dual','sel_flag': 'SL'}),
    

    "Select Action INT": (202, {'select_session': 'S0','query_session': 'S0','select_action': 000,'query_target': 'Dual','sel_flag': 'All'}),

    "Bad Select Action 1": (404, {'select_session': 'S0','query_session': 'S0','select_action': '002','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 2": (404, {'select_session': 'S0','query_session': 'S0','select_action': '020','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 3": (404, {'select_session': 'S0','query_session': 'S0','select_action': '200','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 4": (404, {'select_session': 'S0','query_session': 'S0','select_action': '123','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 5": (404, {'select_session': 'S0','query_session': 'S0','select_action': 'NO','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 6": (404, {'select_session': 'S0','query_session': 'S0','select_action': 000,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 7": (404, {'select_session': 'S0','query_session': 'S0','select_action': 123,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 8": (404, {'select_session': 'S0','query_session': 'S0','select_action': False ,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 9": (404, {'select_session': 'S0','query_session': 'S0','select_action': 0,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 10": (404, {'select_session': 'S0','query_session': 'S0','select_action': 10 ,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 11": (404, {'select_session': 'S0','query_session': 'S0','select_action': '1001','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 12": (404, {'select_session': 'S0','query_session': 'S0','select_action': '9','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 13": (404, {'select_session': 'S0','query_session': 'S0','select_action': 1,'query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Action 14": (404, {'select_session': 'S0','query_session': 'S0','select_action': 100 ,'query_target': 'Dual','sel_flag': 'All'}),

    "Bad Select Session 1": (404, {'select_session': 'S4','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Session 2": (404, {'select_session': 'Bad','query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Session 3": (404, {'select_session': 0,'query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Select Session 4": (404, {'select_session': True,'query_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),

    "Bad Query Session 1": (404, {'select_session': 'S0','query_session': 'S4','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Query Session 2": (404, {'select_session': 'S0','query_session': 'Bad','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Query Session 3": (404, {'select_session': 'S0','query_session': 0,'select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Query Session 4": (404, {'select_session': 'S0','query_session': True ,'select_action': '000','query_target': 'Dual','sel_flag': 'All'}),

    "Bad Query Target 1": (404, {'select_session': 'S0','query_session': 'S4','select_action': '000','query_target': 'C','sel_flag': 'All'}),
    "Bad Query Target 2": (404, {'select_session': 'S0','query_session': 'Bad','select_action': '000','query_target': 0,'sel_flag': 'All'}),
    "Bad Query Target 3": (404, {'select_session': 'S0','query_session': 0,'select_action': '000','query_target': True,'sel_flag': 'All'}),

    "Bad Flag 1": (404, {'select_session': 'S0','query_session': 'S4','select_action': '000','query_target': 'Dual','sel_flag': 'Bad'}),
    "Bad Flag 2": (404, {'select_session': 'S0','query_session': 'Bad','select_action': '000','query_target': 'Dual','sel_flag': 0}),
    "Bad Flag 3": (404, {'select_session': 'S0','query_session': 0,'select_action': '000','query_target': 'Dual','sel_flag': True}),
    
    "Bad Json 1": (400, {'bad_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}), 
    "Bad Json 2": (400, {'select_session': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All', "Extra": "Data"}),
    "Bad Json 3": (400, {'select_session   ': 'S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Bad Json 4": (404, {'select_session': ' S1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    #Leading or trailing space on data in JSON will cause a 404, on column it will cause 400

    "Missing Data 1": (404, {'select_session': '','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Missing Data 2": (404, {'select_session': 'S0','query_session': '','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Missing Data 3": (404, {'select_session': 'S0','query_session': 'S1','select_action': '','query_target': 'Dual','sel_flag': 'All'}),
    "Missing Data 4": (404, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': '','sel_flag': 'All'}),
    "Missing Data 5": (404, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': ''}),

    #"Optional 1": (202, {'query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    #"Optional 2": (202, {'select_session': 'S0','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    #"Optional 3": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','sel_flag': 'All'}),
    #"Optional 4": (202, {'select_session': 'S1','query_session': 'S1', 'query_target': 'Dual','sel_flag': 'All'}),
    #"Optional 5": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'Dual',}),

    "Case Insensitive 1": (202, {'select_session': 's1','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': 'All'}),
    "Case Insensitive 2": (202, {'select_session': 'S0','query_session': 's1','select_action': '000','query_target': 'dual','sel_flag': 'all'}),
    "Case Insensitive 3": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'DUAL','sel_flag': 'All'}),
    "Case Insensitive 4": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'a','sel_flag': 'All'}),
    "Case Insensitive 5": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'b','sel_flag': 'All'}),
    "Case Insensitive 6": (202, {'select_session': 'S0','query_session': 'S1','select_action': '000','query_target': 'Dual','sel_flag': '~sl'}),

}


def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
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
         "{}/***/v0/rain/sel".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    print(response_body, response.status_code)
    if message == "Select Action INT":
        response_body["select_action"] = float(response_body["select_action"])
        check.equal(payload, response_body, message)
    else:
        payload2 = {k.upper():v.upper() for k,v in payload.items()}
        response_body2 = {k.upper():v.upper() for k,v in response_body.items()}
        check.equal(payload2, response_body2, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]         
        poster(message, err, payload, args, ver)
        test_count += 1
    return test_count


def test_select(ip, serial, tout, do_reset, ssl, ver):
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