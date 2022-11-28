from datetime import datetime
import os

import ezconfig.config
#from nose.tools import assert_raises # Not working for some reason
import testdata
import unittest

class TestConfigBasic(unittest.TestCase):

    def test_basic_config(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        assert config.get("basic", "foo") == "1"
        assert config.get("basic", "multiword_with_comment") == "san francisco"
        assert config.get("basic", "whitespace_at_end") == "san francisco"

        return

    def test_defaults_and_mandatories(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        SEC = "basic"
        MISSING_KEY = "no bueno"

        assert config.get(SEC, MISSING_KEY, default=None) is None
        assert config.get(SEC, MISSING_KEY, mandatory=False) is None
        assert config.get(SEC, MISSING_KEY, default="DEFAULT") == "DEFAULT"

        assert config.get(SEC, MISSING_KEY, default="1.0", type=float) == 1.0
        assert config.get(SEC, MISSING_KEY, default=1.0, type=float) == 1.0


        assert config.get("conversions", "val1", mandatory=True) == "1"

        with self.assertRaises(KeyError):
            config.get("conversions", MISSING_KEY, mandatory=True)

        with self.assertRaises(KeyError):
            # mandatory=True has precedence over default value
            assert config.get("conversions", MISSING_KEY, mandatory=True, default=1)

        assert config.get(SEC, MISSING_KEY, default=".", is_filename=True) == \
            os.path.join(os.path.split(__file__)[0], "testdata")

    def test_conversions_and_basic_features(self):
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
        assert config.get("conversions", "val11", raw=True) == "lambda x: x * 2 # With comment"



        assert config.get("raw_values", "val1", raw=True) == "rawval"
        assert config.get("raw_values", "val2", raw=True) == "rawval # With a comment"
        assert config.get("raw_values", "val3", raw=True) == "rawval       # With whitespace"
        assert config.get("raw_values", "val4_trailingwhitespace", raw=True) == "rawval#123"


        assert config.get("conversions", "val_hex1", is_int_hex_str=True) == 10
        assert config.get("conversions", "val_hex2", is_int_hex_str=True) == 16
        assert config.get("conversions", "val_hex_array", is_list=True, is_int_hex_str=True) == [10, 16]

        assert config.get("conversions", "key_val_type2_1") == "foo"
        assert config.get("conversions", "key_val_type2_2", is_list=True, is_timedelta = True) == [1.0, 60.0, 3600.0]

        assert config.get("conversions", "dont_do_this_you_idiot", is_code=True)(3) == 5

        assert config.get("conversions", "date1", is_datetime=True) == datetime(1981, 3, 30)
        assert config.get("conversions", "date2", is_datetime=True) == datetime(1981, 3, 30, 12, 15)
        assert config.get("conversions", "date3", is_datetime=True) == datetime(1981, 3, 30, 12, 13, 14)
        assert config.get("conversions", "date3") == "1981-03-30 12:13:14"



        return


    def test_overrides(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        assert config.get("overrides_in_section", "override_x") == "second_value"
        assert config.get("overrides_in_section", "override_y") == "second_value"

    def test_overrides_between_sections(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)
        assert config.get("conversions", "val1") == "1"


    def test_lists(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        SEC = "list_handling_with_defaults"

        assert config.get(SEC, "string_list", is_list=True) == ["jesus", "mary", "joseph"]
        assert config.get(SEC, "float_list", is_list=True, type=float) == [1.2, 3.14, 5.19]

        assert config.get(SEC, "WTF", is_list=True, default=None) is None
        assert config.get(SEC, "WTF", is_list=True, mandatory=False) is None
        assert config.get(SEC, "WTF", is_list=True, type=int, default=None) is None
        assert config.get(SEC, "WTF", is_list=True, type=int, mandatory=False) is None
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


    def test_static_param(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        assert config.get("static_stuff", "test_fn", raw=True) == "../testdata/default.conf   # A comment"
        assert config.get("static_stuff", "test_fn", static=True) == test_fn
        assert config.get("static_stuff", "test_file", static=True) == test_fn
        assert config.get("static_stuff", "test_var", static=True) == "../testdata/default.conf"



    def test_help_comments(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)
        config.get_key_help("some_help_comments", "string_list") == ""
        config.get_key_help("some_help_comments", "dates") == ""
        config.get_key_help("some_help_comments", "intervals") == "A help comment"


    def test_boolean_values(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        SECTION = "boolean_values"

        assert config.get(SECTION, "key_false_as_int", type=bool) == False
        assert config.get(SECTION, "key_true_as_int", type=bool) == True
        assert config.get(SECTION, "key_true", type=bool) == True
        assert config.get(SECTION, "key_True", type=bool) == True
        assert config.get(SECTION, "key_t", type=bool) == True
        assert config.get(SECTION, "key_T", type=bool) == True

        with self.assertRaises(ValueError):
            assert config.get(SECTION, "key_misspelled_true", type=bool) == False

        with self.assertRaises(ValueError):
            assert config.get(SECTION, "key_misspelled_false", type=bool) == False

        with self.assertRaises(ValueError):
            assert config.get(SECTION, "key_blank_contents", type=bool) == False

        assert config.get(SECTION, "key_false", type=bool) == False
        assert config.get(SECTION, "key_False", type=bool) == False
        assert config.get(SECTION, "key_f", type=bool) == False
        assert config.get(SECTION, "key_F", type=bool) == False

        assert config.get(SECTION, "key_float_zero_is_false", type=bool) == False
        assert config.get(SECTION, "key_float_one_is_true", type=bool) == True
        assert config.get(SECTION, "key_negative_float_is_true", type=bool) == True

        return



    def test_list_behavior(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        SECTION = "list_tests"

        assert config.get(SECTION, "list1", is_list=True) == ["a", "b", "c"]
        assert config.get(SECTION, "list2", is_list=True) == ["a", "b", "c"]
        assert config.get(SECTION, "list3", is_list=True) == ["a", "b", "c"]
        assert config.get(SECTION, "list4", is_list=True) == ["1", "2", "3"]
        assert config.get(SECTION, "list5", is_list=True) == ["1", "2", "3"]

        assert config.get(SECTION, "list4", is_list=True, type=int) == [1,2,3]
        assert config.get(SECTION, "list5", is_list=True, type=int) == [1,2,3]

        assert config.get(SECTION, "NOEXISTO", is_list=True, type=int, default=[1,2,3]) == [1,2,3]




        return
