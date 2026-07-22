import testdata
import os
from pathlib import Path
import ezconfig.config
import pytest

def test_find_test_files():
    test_fn = Path(testdata.get_default_test_config_filename())
    assert test_fn.is_file()
    return


def test_missing_files_throw_exceptions():
    good_fn = testdata.get_default_test_config_filename()
    bad_fn = "/a/b/c/d"


    assert ezconfig.config.ConfigurationFile(good_fn)
    with pytest.raises(IOError):
        ezconfig.config.ConfigurationFile(bad_fn)

    return
