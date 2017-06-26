# Copyright (C) Windfall Technology - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

# Python 3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ConfigParser import ConfigParser
import os

import atlas.exceptions
import local  # NOQA

__author__ = "Nathan Addy <nathan.addy@gmail.com>"

"""
Provide the Configuration class for the application
"""


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

        if not os.path.isfile(fn):
            err_msg = "No such file: '{}' -> '{}'".format(fn, self.filename)
            raise atlas.exceptions.MissingConfigurationFileXcpt(err_msg)

        self._conf = ConfigParser()
        self._conf.read(self.filename)
        return

    def sections(self):
        '''Return the configuration section titles'''
        return self._conf.sections()

    def get(self, sect, key, default=False, mandatory=False,
            type=False, is_filename=False, is_timedelta=False, raw=False):
        '''Primary class method for reading values in the configuration file.

        Supports commenting, typecasting, default-values, mandatory
        values, and a variety of other features.

        sect, key - str, section and key to look up value
        default - value returned if sect::key does not exist in the config file
        mandatory - raises exception if sect::key is not present
        type - convert value to key_type
        is_filename - return absolute path for filename in sect::key
        is_timedelta - allow values like 3w or 3d 4h 13n 57s
        raw - do not do any variable substitutions when extracting the value
        '''

        if mandatory and not self.has(sect, key):
            err_msg = "Missing configuration exception '{0}::{1}'".format(sect, key)
            raise atlas.exceptions.MissingConfigurationKeyXcpt(err_msg)

        value = default
        if self._conf.has_option(sect, key):
            value = self._strip_comment(self._conf.get(sect, key, raw))

        if is_filename and value:
            value = os.path.abspath(os.path.join(self.base_dir, value))

        if type:
            value = type(value)

        if is_timedelta:
            value = Configuration._getBestSecondsFromConfigString(value)

        return value

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
