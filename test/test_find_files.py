import testdata
import os

def test_find_test_files():
    test_fn = testdata.get_default_test_config_filename()
    assert os.path.isfile(test_fn)
    return
