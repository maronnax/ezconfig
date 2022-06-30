import os

def get_test_directory():
    return os.path.join(os.path.split(__file__)[0], "testdata")

def get_default_test_config_filename():
    return os.path.join(get_test_directory(), "default.conf")

def get_comp1_test_config_filename():
    return os.path.join(get_test_directory(), "conf1.conf")

def get_comp2_test_config_filename():
    return os.path.join(get_test_directory(), "conf2.conf")

def get_comp3_test_config_filename():
    return os.path.join(get_test_directory(), "conf3.conf")


def get_conf_configuration_set_defaults1():
    return os.path.join(get_test_directory(), "conf_multidef1.conf")

def get_conf_configuration_set_defaults2():
    return os.path.join(get_test_directory(), "conf_multidef2.conf")
