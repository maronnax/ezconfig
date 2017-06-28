import testdata
import ezconfig.config
from datetime import datetime
import os

def test_basic_config():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)

    assert config.get("basic", "foo") == "1"
    assert config.get("basic", "multiword_with_comment") == "san francisco"
    assert config.get("basic", "whitespace_at_end") == "san francisco"

    return


def test_conversions():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)
    assert config.get("conversions", "val0") == "string"
    assert config.get("conversions", "val1") == "1"
    assert config.get("conversions", "val1", type=int) == 1
    assert config.get("conversions", "val1", type=float) == 1.0
    assert config.get("conversions", "val2", type=float) == 3.1415
    assert config.get("conversions", "val4", is_timedelta=True) == 10.0
    assert config.get("conversions", "val5", is_timedelta=True) == 60 * .25
    assert config.get("conversions", "val6", is_timedelta=True) == 3600
    assert config.get("conversions", "val7", is_timedelta=True) == (3 * 24 * 3600)
    assert config.get("conversions", "val77", is_timedelta=True) == (3 * 7 * 24 * 3600)
    assert config.get("conversions", "val8", is_filename=True) == test_fn
    assert config.get("conversions", "val9", is_filename=True) == test_fn
    assert config.get("conversions", "val10", is_filename=True) == "/usr/bin/env"
    assert config.get("conversions", "val10", is_filename=True) == "/usr/bin/env"

    f = config.get("conversions", "val11", is_code=True)
    assert f(1) == 2
    assert config.get("conversions", "val11", raw=True) == "lambda x: x * 2"


    assert config.get("conversions", "date1", is_datetime=True) == datetime(1981, 3, 30)
    assert config.get("conversions", "date2", is_datetime=True) == datetime(1981, 3, 30, 12, 15)
    assert config.get("conversions", "date3", is_datetime=True) == datetime(1981, 3, 30, 12, 13, 14)
    assert config.get("conversions", "date3") == "1981-03-30 12:13:14"

    return
