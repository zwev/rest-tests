# This test posts every combination of valid advanced settings to the reader and checks that invalid advanced settings do not post.
# It also checks that returned settings match what was posted.

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
    
    "Good Advanced T  0-0; 50": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced T  0-0; 100": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced T  0-0; 200": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced T  0-0; 400": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced T  0-1; 50": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced T  0-1; 100": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced T  0-1; 200": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced T  0-1; 400": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced T  0-2; 50": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced T  0-2; 100": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced T  0-2; 200": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced T  0-2; 400": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced T  0-3; 50": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced T  0-3; 100": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced T  0-3; 200": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced T  0-3; 400": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced T  0-4; 50": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced T  0-4; 100": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced T  0-4; 200": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced T  0-4; 400": (202, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 400}),
   
    "Good Advanced T  1-0; 50": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced T  1-0; 100": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced T  1-0; 200": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced T  1-0; 400": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced T  1-1; 50": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced T  1-1; 100": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced T  1-1; 200": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced T  1-1; 400": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced T  1-2; 50": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced T  1-2; 100": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced T  1-2; 200": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced T  1-2; 400": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced T  1-3; 50": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced T  1-3; 100": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced T  1-3; 200": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced T  1-3; 400": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced T  1-4; 50": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced T  1-4; 100": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced T  1-4; 200": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced T  1-4; 400": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced T  2-0; 50": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced T  2-0; 100": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced T  2-0; 200": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced T  2-0; 400": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced T  2-1; 50": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced T  2-1; 100": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced T  2-1; 200": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced T  2-1; 400": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced T  2-2; 50": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced T  2-2; 100": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced T  2-2; 200": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced T  2-2; 400": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced T  2-3; 50": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced T  2-3; 100": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced T  2-3; 200": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced T  2-3; 400": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced T  2-4; 50": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced T  2-4; 100": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced T  2-4; 200": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced T  2-4; 400": (202, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced T  3-0; 50": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced T  3-0; 100": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced T  3-0; 200": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced T  3-0; 400": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced T  3-1; 50": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced T  3-1; 100": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced T  3-1; 200": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced T  3-1; 400": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced T  3-2; 50": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced T  3-2; 100": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced T  3-2; 200": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced T  3-2; 400": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced T  3-3; 50": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced T  3-3; 100": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced T  3-3; 200": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced T  3-3; 400": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced T  3-4; 50": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced T  3-4; 100": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced T  3-4; 200": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced T  3-4; 400": (202, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced T  4-0; 50": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced T  4-0; 100": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced T  4-0; 200": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced T  4-0; 400": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced T  4-1; 50": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced T  4-1; 100": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced T  4-1; 200": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced T  4-1; 400": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced T  4-2; 50": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced T  4-2; 100": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced T  4-2; 200": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced T  4-2; 400": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced T  4-3; 50": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced T  4-3; 100": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced T  4-3; 200": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced T  4-3; 400": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced T  4-4; 50": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced T  4-4; 100": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced T  4-4; 200": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced T  4-4; 400": (202, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced F  0-0; 50": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced F  0-0; 100": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced F  0-0; 200": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced F  0-0; 400": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced F  0-1; 50": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced F  0-1; 100": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced F  0-1; 200": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced F  0-1; 400": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced F  0-2; 50": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced F  0-2; 100": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced F  0-2; 200": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced F  0-2; 400": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced F  0-3; 50": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced F  0-3; 100": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced F  0-3; 200": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced F  0-3; 400": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced F  0-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced F  0-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced F  0-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced F  0-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': 0, 'preselect_count': 4}, 'hopping_interval': 400}),
   
    "Good Advanced F  1-0; 50": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced F  1-0; 100": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced F  1-0; 200": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced F  1-0; 400": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced F  1-1; 50": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced F  1-1; 100": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced F  1-1; 200": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced F  1-1; 400": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced F  1-2; 50": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced F  1-2; 100": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced F  1-2; 200": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced F  1-2; 400": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced F  1-3; 50": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced F  1-3; 100": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced F  1-3; 200": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced F  1-3; 400": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced F  1-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced F  1-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced F  1-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced F  1-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': 1, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced F  2-0; 50": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced F  2-0; 100": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced F  2-0; 200": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced F  2-0; 400": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced F  2-1; 50": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced F  2-1; 100": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced F  2-1; 200": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced F  2-1; 400": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced F  2-2; 50": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced F  2-2; 100": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced F  2-2; 200": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced F  2-2; 400": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced F  2-3; 50": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced F  2-3; 100": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced F  2-3; 200": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced F  2-3; 400": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced F  2-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced F  2-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced F  2-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced F  2-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': 2, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced F  3-0; 50": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced F  3-0; 100": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced F  3-0; 200": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced F  3-0; 400": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced F  3-1; 50": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced F  3-1; 100": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced F  3-1; 200": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced F  3-1; 400": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced F  3-2; 50": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced F  3-2; 100": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced F  3-2; 200": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced F  3-2; 400": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced F  3-3; 50": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced F  3-3; 100": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced F  3-3; 200": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced F  3-3; 400": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced F  3-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced F  3-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced F  3-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced F  3-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': 3, 'preselect_count': 4}, 'hopping_interval': 400}),
 
    "Good Advanced F  4-0; 50": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Good Advanced F  4-0; 100": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 100}),
    "Good Advanced F  4-0; 200": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Good Advanced F  4-0; 400": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 0}, 'hopping_interval': 400}),
 
    "Good Advanced F  4-1; 50": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Good Advanced F  4-1; 100": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 100}),
    "Good Advanced F  4-1; 200": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 200}),
    "Good Advanced F  4-1; 400": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 1}, 'hopping_interval': 400}),
 
    "Good Advanced F  4-2; 50": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 50}),
    "Good Advanced F  4-2; 100": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 100}),
    "Good Advanced F  4-2; 200": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 200}),
    "Good Advanced F  4-2; 400": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 2}, 'hopping_interval': 400}),
 
    "Good Advanced F  4-3; 50": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 50}),
    "Good Advanced F  4-3; 100": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 100}),
    "Good Advanced F  4-3; 200": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 200}),
    "Good Advanced F  4-3; 400": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 3}, 'hopping_interval': 400}),
 
    "Good Advanced F  4-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 50}),
    "Good Advanced F  4-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 100}),
    "Good Advanced F  4-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 200}),
    "Good Advanced F  4-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': 4, 'preselect_count': 4}, 'hopping_interval': 400}),

    "Good Advanced STR 4-4; 50": (202, {'drm_active': False, 'select_setup': {'mode': "4", 'preselect_count': "4"}, 'hopping_interval': "50"}),
    "Good Advanced STR 4-4; 100": (202, {'drm_active': False, 'select_setup': {'mode': "4", 'preselect_count': "4"}, 'hopping_interval': "100"}),
    "Good Advanced STR 4-4; 200": (202, {'drm_active': False, 'select_setup': {'mode': "4", 'preselect_count': "4"}, 'hopping_interval': "200"}),
    "Good Advanced STR 4-4; 400": (202, {'drm_active': False, 'select_setup': {'mode': "4", 'preselect_count': "4"}, 'hopping_interval': "400"}),
 
    "Missing Nothing": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Missing Select Mode": (202, {'drm_active': True, 'select_setup': {'preselect_count': 1}, 'hopping_interval': 50}),
    "Missing Select Count": (202, {'drm_active': True, 'select_setup': {'mode': 1,}, 'hopping_interval': 50}),
    "Missing DRM": (202, {'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 50}),
    "Missing Hopping": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}}),
    "Missing Selects": (202, {'drm_active': True, 'hopping_interval': 50}),
    "Missing Setup + Hopping": (202, {'drm_active': True,}),
    "Missing DRM + Hopping": (202, {'select_setup': {'mode': 1, 'preselect_count': 1},}),
    "Missing DRM + Selects": (202, {'hopping_interval': 50}),

    "Bad Selects T  0-999; 50": (404, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 999}, 'hopping_interval': 50}),
    "Bad Selects T  1-Str; 50": (404, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': "4"}, 'hopping_interval': 50}),
    "Bad Selects T  2-Bool; 50": (404, {'drm_active': True, 'select_setup': {'mode': 2, 'preselect_count': True,}, 'hopping_interval': 50}),
    "Bad Selects T  3-Empty; 50": (404, {'drm_active': True, 'select_setup': {'mode': 3, 'preselect_count': ""}, 'hopping_interval': 50}),
    "Bad Selects T  4_-1; 50": (404, {'drm_active': True, 'select_setup': {'mode': 4, 'preselect_count': -1}, 'hopping_interval': 50}),
    "Bad Selects T  999-0; 50": (404, {'drm_active': True, 'select_setup': {'mode': 999, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Bad Selects T  Str-1; 50": (404, {'drm_active': True, 'select_setup': {'mode': "4", 'preselect_count': 0}, 'hopping_interval': 50}),
    "Bad Selects T  Bool-2; 50": (404, {'drm_active': True, 'select_setup': {'mode': True, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Bad Selects T  Empty-3; 50": (404, {'drm_active': True, 'select_setup': {'mode': "", 'preselect_count': 0}, 'hopping_interval': 50}),
    "Bad Selects T  -1_4; 50": (404, {'drm_active': True, 'select_setup': {'mode': -1, 'preselect_count': 0}, 'hopping_interval': 50}),
    "Bad Selects T 11-11; 200": (404, {'drm_active': True, 'select_setup': {'mode': 11, 'preselect_count': 11}, 'hopping_interval': 200}),
    "Bad Selects T -1_-1; 200": (404, {'drm_active': True, 'select_setup': {'mode': -1, 'preselect_count': -1}, 'hopping_interval': 200}),
    "Bad Selects T 11-0; 200": (404, {'drm_active': True, 'select_setup': {'mode': 11, 'preselect_count': 0}, 'hopping_interval': 200}),
    "Bad Selects T 0-11; 200": (404, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': 11}, 'hopping_interval': 200}),
    #"Bad Advanced T Bool-0; 200": (404, {'drm_active': True, 'select_setup': {'mode': True, 'preselect_count': 0}, 'hopping_interval': 200}),
    #"Bad Advanced T 0-Bool; 200": (404, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': True}, 'hopping_interval': 200}),
    #"Bad Advanced T Str-0; 200": (404, {'drm_active': True, 'select_setup': {'mode': 0, 'preselect_count': "0"}, 'hopping_interval': 200}),
    #"Bad Advanced T 0-Str; 200": (404, {'drm_active': True, 'select_setup': {'mode': "0", 'preselect_count': 0}, 'hopping_interval': 200}),



    "Bad Hopping": (404, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 3900}), 
    

    "Bad DRM": (400, {'drm_active': "True", "select_setup": {'mode': 1, 'preselect_count': 1}, 'hoping_interval': 400}),
    "Bad DRM2": (404, {'drm_active': 15, "select_setup": {'mode': 1, 'preselect_count': 1}, 'hoping_interval': 400}),
    "Bad Hopping 2": (404, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 150}),
    #"+Bad json": (202, {'drm_active': True,}),
    # I printed the status code before the logic in poster and it seems like it accepts even though mode and preselect count are missing and returns a 202
    "Bad Json 1": (400, {'drm_active': True, 'select_setup': {'': 1, 'preselect_count': 1}, 'hopping_interval': 400}),
    "Bad Json 2": (400, {}),
    #"+Bad Json 3": (202, {'drm_active': True, 'select_setup': {'mode': 1, 'preselect_count': 1}}),
    #Same as above
    "Bad Json4": (400, {'drm_active': True, False: {'mode': 1, 'preselect_count': 1}, 'hopping_interval': 400}),
    "Bad Json5": (400, {'drm_active': True, "select_setup": {'mode': 1, 'preselect_count': 1}, 'hoping_interval': 400}),
    "Bad Json6": (400, {'drm_active': True, "select_setup": {'mode': 1, 'preselect_count': 1}, 'hoping_interval': 400}),
    }


def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/rain/adv".format(sec),
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
         "{}/***/v0/rain/adv".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         timeout=args['timeout'], verify=ver
         )
    response_body = response.json()
    if "Good Advanced STR" in message:
        payload.pop('drm_active')
        response_body.pop('drm_active')
        payload2 = {k:float(v) for k,v in payload['select_setup'].items()}
        payload2['hopping_interval'] = str(payload['hopping_interval'])
        response_body2 = {k:float(v) for k,v in response_body['select_setup'].items()}
        response_body2['hopping_interval'] = str(response_body['hopping_interval'])
        check.equal(payload2, response_body2, message)
    else:
        check.equal(payload, response_body, message)

def unpacker(params, args, ver):
    test_count = 0
    for x, y in params.items():
        message = x
        err = y[0]
        payload = y[1]         
        poster(message, err, payload, args, ver)
        test_count += 1
    return test_count


def test_advanced(ip, serial, tout, do_reset, ssl, ver):
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
