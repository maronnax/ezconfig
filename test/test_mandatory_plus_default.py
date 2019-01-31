from datetime import datetime
import os

import pdb
import ezconfig.config
#from nose.tools import assert_raises # Not working for some reason
import testdata
import unittest

class TestConfigBasic(unittest.TestCase):
    def test_basic_config(self):
        test_fn = testdata.get_default_test_config_filename()
        config = ezconfig.config.Configuration(test_fn)

        SECTION = "basic"
        MISSING_KEY = "missing key"
        MISSING_SECTION = "missing section"

        assert config.get(SECTION, MISSING_KEY, default = 10) == 10
        assert config.get(MISSING_SECTION, MISSING_KEY, default = 10) == 10
        assert config.get(SECTION, MISSING_KEY, mandatory=False) == None
        assert config.get(SECTION, MISSING_KEY, mandatory=False, default=10) == 10
        assert config.get(SECTION, "foo", default = 10, mandatory=True, type=int) == 1
