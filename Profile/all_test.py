# This test posts a valid/invalid JSON data to the reader to set all Antenna and RAIN settings and checks that invalid settings do not get saved.
# It also checks that returned sequence is what was posted.
# One thing this test does slightly differently than the rest is take JSON data for the default settings from the conftest.py file.
# The tuple containing "None" for "Default Settings" in params is set to the expected 202 error code as well as the default settings JSON at test collection. 
# A similar method can be used to store other non-default settings if needed.

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


params = {"Default Settings": (None),
"Bad Antenna": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "4",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Power": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "4.50"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad RF": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Select Target 1": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "C",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Select Target 2": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": True,
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Select Action 1": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Q Dynamic Str": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": "BAD",
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Q Static Negative": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "static",
      "start_q": -10,
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 400
    }
  }
}),
"Bad Advanced Hopping 3900": (404, {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": "500",      
    "power_levels": [
      {
        "antenna_id": "0",    
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "1",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "2",
        "read_power": "30.00",
        "write_power": "30.00"
      },
      {
        "antenna_id": "3",
        "read_power": "30.00",
        "write_power": "30.00"
      }
    ]
  },
  "rain": {
    "rfmode": {
      "rfmode": "1", "est_tag_pop": "300"
    },
    "q_algorithm": {
      "algo_type": "dynamic",
      "start_q": 3,
      "min_q": 0,
      "max_q": 15
    },
    "select_control": {
      "select_session": "S1",
      "query_session": "S1",
      "select_action": "000",
      "query_target": "Dual",
      "sel_flag": "All"
    },
    "advanced": {
      "drm_active": True,
      "select_setup": {
        "mode": 1,
        "preselect_count": 1
      },
      "hopping_interval": 3900
    }
  }
}),
}

def poster(message, err, payload, args, ver):
    response = requests.post(
         "{}/***/v0/profile/rfid".format(sec),
         headers={"Authorization": "Bearer " + args["serial"]},
         json=payload,
         timeout=args['timeout'], verify=ver
         )
    print(message, "==>", payload, response.status_code, "\n")
    if err == response.status_code and response.status_code >= 200 and response.status_code < 210:
        getter(message,payload, args, ver)
    else:
        check.equal(err, response.status_code, message)

def getter(message, payload, args, ver):
    response = requests.get(
         "{}/***/v0/profile/rfid".format(sec),
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
        poster(message, err, payload, args, ver)
        test_count += 1
    return test_count

def setter(args):
  return args

def test_all(ip, serial, tout, do_reset, defaultset, ssl, ver):
    args = {"ip":ip, "serial":serial, "timeout":tout}
    global sec
    sec = "http{}://{}".format(str(ssl), args['ip'])
    do_reset = True
    if "s" in sec:
        ssl_reset(args, ssl, ver)
    if do_reset and "s" not in sec:
        factory_reset(args)
    global params
    params['Default Settings'] = (202, setter(defaultset))
    print("")
    test_count = unpacker(params, args, ver)
    print("")
    print("Ran ", test_count, " tests")


  