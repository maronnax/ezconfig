from datetime import datetime
import os

import pdb
import ezconfig.config
import testdata

def test_config_composion():
    comp1_fn = testdata.get_comp1_test_config_filename()
    comp2_fn = testdata.get_comp2_test_config_filename()
    comp3_fn = testdata.get_comp3_test_config_filename()
    config = ezconfig.config.ConfigurationSet(comp1_fn, comp2_fn, comp3_fn)

    assert config
