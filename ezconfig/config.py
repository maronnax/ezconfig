# Copyright (C) Windfall Technology - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Python 3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser
import itertools
import collections
import os

import dateutil.parser

__author__ = "Nathan Addy <nathan.addy@gmail.com>"

"""
Provide the Configuration class for the application
"""

MANDATORY_PLUS_DEFAULT_ERROR_MSG = "mandotory cannot be true while default is not None"
STATIC_WITH_OTHER_PARAMS_ERROR_MSG = "static=True must not be passed with other parameters"

def _convert_to_integer(obj):
  try:
    return int(obj)
  except ValueError:
    return int(obj, 16)

class Configuration(object):

    '''Represents a configuration object that holds values in the form
    section::key.

    The main class method is get, which allows for getting values with
    a default and also has build-in methods for automatically
    processing values found in the configuration.

    '''

    def __init__(self, fn):
        self.filename = os.path.abspath(fn)
        self.base_dir = os.path.abspath(os.path.split(fn)[0])
        self.static_filename_key_indicators = ["_fn", "_file"]

        if not os.path.isfile(fn):
            err_msg = "No such file: '{}'".format(self.filename)
            raise IOError(err_msg)

        self._conf = ConfigParser()
        self._conf.read(self.filename)
        return

    def sections(self):
        '''Return the configuration section titles'''
        return self._conf.sections()

    def variables(self):
        '''Return a list of (section, keys) in the configuration file'''
        return list(itertools.chain.from_iterable(map(lambda sec: (map(lambda (var,val): (sec, var),
                                                                       self._conf.items(sec))),
                                                      self._conf.sections())))

    # Do not want to enable this for now, as this returns the raw values and is this not at all EZ.
    # def items(self):
    #     return list(itertools.chain.from_iterable(map(lambda sec: (map(lambda (var,val): (sec, var, val),
    #                                                                    self._conf.items(sec))),
    #                                                   self._conf.sections())))


    def get(self, sect, key, default=None, mandatory=False,
            type=False, is_filename=False, is_timedelta=False, is_datetime=False,
            is_list=False, raw=False, is_int_hex_str=False, is_code=False, static=False):

        '''Primary class method for reading values in the configuration file.

        Supports commenting, typecasting, default-values, mandatory
        values, and a variety of other features.

        sect, key - str, section and key to look up value
        default - value returned if sect::key does not exist in the config file
        mandatory - raises exception if sect::key is not present
        type - convert value to key_type
        is_filename - return absolute path for filename in sect::key
        is_timedelta - allow values like 3w or 3d 4h 13n 57s
        is_list - Assume the value is a "string" list: first the string will be split
                  by ","; if set, each element is cast to `type` param.
        is_code - Assume that this is a string representing a lambda object in python
                  and that we can eval the value to product a function in python.
        is_int_hex_str: This is a string that specifies an integer in either decimal
                        or hex.  E.g. "193" (decimal) or "0xc1" both return the 193.
        raw - do not do any variable substitutions when extracting the value

        static - if set to true the class will act as though the field is raw unless the key
                 matches `static_filename_key_indicators`, in which case filename=True is used.
        '''

        # NJA-TAG Change this
        if mandatory and default is not None:
            raise ValueError(MANDATORY_PLUS_DEFAULT_ERROR_MSG)

        if static == True and filter(lambda x: False, (type, is_filename, is_timedelta, is_code,
                                                       is_int_hex_str, raw)):
            raise ValueError(STATIC_WITH_OTHER_PARAMS_ERROR_MSG)

        if mandatory and not self.has(sect, key):
            err_msg = "Missing configuration exception '{0}::{1}'".format(sect, key)
            raise KeyError(err_msg)

        if not self.has(sect, key):
            value = default
            if value is None: return
        else:
            value = self._conf.get(sect, key)

        if static:
            if filter(lambda fnend: key.strip().endswith(fnend), self.static_filename_key_indicators):
                return self.parse_string(value, is_filename = True)
            else:
                return self._strip_comment(value)

        return self.parse_string(value, type, is_filename, is_timedelta, is_datetime,
                                 is_list, raw, is_int_hex_str, is_code)


    def parse_string(self, value, type=False, is_filename=False, is_timedelta=False, is_datetime=False,
                     is_list=False, raw=False, is_int_hex_str=False, is_code=False):

        # Because of the refactor the caller can potentially put a default value in here and
        # we need to handle it.
        if isinstance(value, str):
            value = self._strip_comment(value)

        if is_list:
            if value == "" or value == "()" or value == "[]":
                value_list = []
            else:
                value_list = map(lambda str: str.strip(), value.split(","))
        else:
            value_list = [value]

        if is_filename:
            value_list = map(
                lambda val: os.path.abspath(os.path.join(self.base_dir, os.path.expanduser(val))),
                value_list
            )

        if is_int_hex_str:
            value_list = map(_convert_to_integer, value_list)
        if type:
            value_list = map(type, value_list)

        if is_timedelta:
            value_list = map(lambda val: Configuration._getBestSecondsFromConfigString(val), value_list)

        if is_datetime:
            value_list = map(lambda val: dateutil.parser.parse(val), value_list)

        if is_code:
            value_list = map(eval, value_list)

        if not is_list:
            return value_list[0] if value_list else default
        else:
            if value_list:
                return value_list
            else:
                if value == "":
                    return []
                elif value is None:
                    return None
                else:
                    return value_list


    def has(self, sect, key):
        '''Check if sect::key is present in the config object'''
        return self._conf.has_option(sect, key)

    @staticmethod
    def _getBestSecondsFromConfigString(conf_string):
        '''
        Takes a string like 20, 20.0, 21.3s 29m, 30.1h and returns a
        floating number of seconds.

        Keyword arguments:
        conf (str): A string representing a number using the [A<.B>[ shmd] syntax.

        Returns:
        float: the number of seconds represented by the string
        '''

        conf_string = conf_string.strip()

        # S,M,H,D,T=1,2,3,4,5
        # interval = S

        if conf_string[-1].lower() not in "smdhwy":
            return float(conf_string)

        float_str, val = conf_string[:-1], conf_string[-1].lower()

        if val == "s":
            return float(float_str)
        elif val == "m":
            return float(float_str) * 60
        elif val == "h":
            return float(float_str) * 3600
        elif val == "d":
            return float(float_str) * 3600 * 24
        elif val == "w":
            return float(float_str) * 3600 * 24 * 7
        elif val == "y":
            return float(float_str) * 3600 * 24 * 365
        else:
            raise Exception("Unknown error")

        return

    def _strip_comment(self, string_value):
        '''Remove any comments starting with the '#' character'''
        if "#" in string_value:
            ndx = string_value.find("#")
            string_value = string_value[:ndx].strip()
        return string_value

class ConfigurationSet(object):
    """configuration files and returns an ezconfig interface that treats
    the files as most_significant to least significant.
    """
    def __init__(self, *config_fn_list):

        # config_fn_lists is stored reversed so scan the files from
        # most->least significant when we get() values.
        self._config_fn_list = map(lambda fn: os.path.abspath(fn), config_fn_list)
        self._config_list = map(lambda fn: Configuration(fn), self._config_fn_list)

        self.config = Configuration(self._config_fn_list[1])

        return

    def sections(self):
        # Python doens't have an OrderedSet so I'm doing the same thing with an OrderedDict.
        section_dict = collections.OrderedDict()
        for section in list(itertools.chain(*map(lambda ez: ez.sections(), self._config_list))):
            section_dict[section] = True
        return section_dict.keys()

    def variables(self):
        variable_dict = collections.OrderedDict()
        for section in list(itertools.chain(*map(lambda ez: ez.variables(), self._config_list))):
            variable_dict[section] = True
        return variable_dict.keys()

    def parse_string(self, *args, **kwds):
        return self._config_list[0].parse_string(*args, **kwds)

    def get(self, *args, **kwds):
        # The only thing here is that we must keep track of
        # mandatory=True.  That makes things a little gross.

        if "mandatory" in kwds and "default" in kwds and kwds["mandatory"] and kwds["default"] is not None:
            raise ValueError(MANDATORY_PLUS_DEFAULT_ERROR_MSG)

        section, key = args[:2]
        potential_values = filter(
            lambda x: x is not None,
            map(lambda conf: conf.get(*args, **dict(kwds.items() + {"mandatory": False}.items())),
                self._config_list))

        if potential_values:
            return potential_values[0]
        else:
            return self._config_list[0].get(*args, **kwds) # This will throw if mandatory=True


    def has(sect, key):
        return True in map(lambda ez: ez.has(sect, key), self._config_list)
