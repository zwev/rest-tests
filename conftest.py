import pytest

@pytest.fixture()
def ip():
    return "***"

@pytest.fixture()
def serial():
    return "***"

@pytest.fixture()
def tout():
    return 18

@pytest.fixture()
def do_reset():
    return False

@pytest.fixture()
def defaultset():
    default = {
  "antenna_setup": {
    "sequence": [
      0
    ],
    "dwell_time": {"dwell_time": "500"},      
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
        "preselect_count": 1,
        },
        "hopping_interval": 400
    }
  }
}
    return default

@pytest.fixture()
def ssl(pytestconfig):
    return pytestconfig.getoption("ssl")

@pytest.fixture()
def tim(pytestconfig):
    return pytestconfig.getoption("tim")

@pytest.fixture()
def ver (pytestconfig):
    return pytestconfig.getoption("ver")

def pytest_addoption(parser):
    parser.addoption("--tim", action="store", default=10)
    parser.addoption("--ssl", action="store_const", const="s", default="")
    parser.addoption('--ver', action="store_true", default=False)
