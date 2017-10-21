from datetime import datetime
import os

import pdb
import ezconfig.config
import testdata

def test_basic_config():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)

    assert config.get("basic", "foo") == "1"
    assert config.get("basic", "multiword_with_comment") == "san francisco"
    assert config.get("basic", "whitespace_at_end") == "san francisco"

    return

def test_defaults_and_mandatories():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)

    SEC = "basic"
    MISSING_KEY = "no bueno"

    assert config.get(SEC, MISSING_KEY) is None
    assert config.get(SEC, MISSING_KEY, default="DEFAULT") == "DEFAULT"

    assert config.get(SEC, MISSING_KEY, default="1.0", type=float) == 1.0
    assert config.get(SEC, MISSING_KEY, default=1.0, type=float) == 1.0

    assert config.get(SEC, MISSING_KEY, default=".", is_filename=True) == \
        os.path.join(os.path.split(__file__)[0], "testdata")

def test_conversions_and_basic_features():
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


def test_overrides():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)

    assert config.get("overrides_in_section", "override_x") == "second_value"
    assert config.get("overrides_in_section", "override_y") == "second_value"

def test_overrides_between_sections():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)
    assert config.get("conversions", "val1") == "1"


def test_lists():
    test_fn = testdata.get_default_test_config_filename()
    config = ezconfig.config.Configuration(test_fn)

    SEC = "list_handling_with_defaults"

    assert config.get(SEC, "string_list", is_list=True) == ["jesus", "mary", "joseph"]
    assert config.get(SEC, "float_list", is_list=True, type=float) == [1.2, 3.14, 5.19]

    assert config.get(SEC, "WTF", is_list=True) is None
    assert config.get(SEC, "WTF", is_list=True, type=int) is None
    assert config.get(SEC, "WTF", is_list=True, default="1,2,3") == ["1", "2", "3"]
    assert config.get(SEC, "WTF", is_list=True, default="1,2,3", type=int) == [1,2,3]

    assert config.get(SEC, "WTF", is_list=True, default="") == []
    assert config.get(SEC, "WTF", is_list=True, default="", type=int) == []


    assert config.get(SEC, "dates", is_list=True, is_datetime=True) == [datetime(1981, 3, 30, 1, 15),
                                                                        datetime(1981, 3, 30, 0, 0),
                                                                        datetime(1981, 3, 30, 1, 30)]

    assert config.get(SEC, "intervals", is_list=True, is_timedelta=True) == \
        [10.0, 10.1, 15, 15, 13*60, 1.5*3600, 10*24*3600, 15*7*24*3600]



    return
