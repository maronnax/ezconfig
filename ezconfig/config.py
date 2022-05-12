# Copyright (C) Windfall Technology

from configparser import ConfigParser
import itertools
import collections
import os
import sys
import re

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

def _convert_string_to_bool(string):
  if string.lower() in ["t", "f", "true", "false"]:
    return string.lower()[0] == "t"
  else:
    return float(string) != 0.0


STATIC_FILENAME_KEY_INDICATORS = ["_fn", "_file"]
class ConfigurationFile(object):

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
            err_msg = "No such file: '{}'".format(self.filename)
            raise IOError(err_msg)

        self._conf = ConfigParser(strict=False)
        self._conf.read(self.filename)
        return

    def sections(self):
        '''Return the configuration section titles'''
        return self._conf.sections()

    def variables(self):
        '''Return a list of (section, keys) in the configuration file'''
        return list(itertools.chain.from_iterable(map(lambda sec: (map(lambda varval: (sec, varval[0]),
                                                                       self._conf.items(sec))),
                                                      self._conf.sections())))

    # Do not want to enable this for now, as this returns the raw values and is this not at all EZ.
    # def items(self):
    #     return list(itertools.chain.from_iterable(map(lambda sec: (map(lambda (var,val): (sec, var, val),
    #                                                                    self._conf.items(sec))),
    #                                                   self._conf.sections())))


    def get(self, sect, key, default=None, mandatory=True,
            type=False, is_filename=False, is_timedelta=False, is_datetime=False,
            is_list=False, raw=False, is_int_hex_str=False, is_code=False, static=False):

        '''Primary class method for reading values in the configuration file.

        Supports commenting, typecasting, default-values, mandatory
        values, and a variety of other features.

        sect, key - str, section and key to look up value
        default - value returned if sect::key does not exist in the config file
        mandatory - raises exception if sect::key is not present
        type - convert value to key_type; type=boolean has special handling for strings
               representing boolean values
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
                 matches `STATIC_FILENAME_KEY_INDICATORS`, in which case filename=True is used.
        '''

        # NJA-TAG check this...
        if static == True and [x for x in (type, is_filename, is_timedelta, is_code,
                                                       is_int_hex_str, raw) if False]:
            raise ValueError(STATIC_WITH_OTHER_PARAMS_ERROR_MSG)

        if mandatory and not self.has(sect, key):
            err_msg = "Missing configuration exception '{0}::{1}'".format(sect, key)
            raise KeyError(err_msg)

        if not self.has(sect, key):
            value = str(default)
            if value is None: return
        else:
            value = self._conf.get(sect, key)

        if static:
            if [fnend for fnend in STATIC_FILENAME_KEY_INDICATORS if key.strip().endswith(fnend)]:
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
            value = re.sub(r"^\s*[\[\(]\s*", "", value)
            value = re.sub(r"[\]\)]\s*$", "", value)

            if value == "" or value == "()" or value == "[]":
                value_list = []
            else:
                value_list = [str.strip() for str in value.split(",")]
        else:
            value_list = [value]

        if is_filename:
            value_list = [os.path.abspath(os.path.join(self.base_dir, os.path.expanduser(val))) for val in value_list]

        if is_int_hex_str:
            value_list = list(map(_convert_to_integer, value_list))
        if type and type != bool:
          value_list = list(map(type, value_list))
        if type and type == bool:
          value_list = list(map(_convert_string_to_bool, value_list))

        if is_timedelta:
            value_list = [ConfigurationFile._getBestSecondsFromConfigString(val) for val in value_list]

        if is_datetime:
            value_list = [dateutil.parser.parse(val) for val in value_list]

        if is_code:
            value_list = list(map(eval, value_list))

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

    def get_key_help(self, section, key):

      if not self.has(section, key): return ""
      value = self._conf.get(section, key)
      if "##" not in value:
        return ""
      else:
        help_key = value[ value.index("##") + 2: ].strip()

        help_key = help_key.replace("##", "")
        help_key = re.sub("\W+", " ", help_key)
        return help_key

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

class Configuration(object):
    """takes a list of configuration files and returns an ezconfig
    interface that treats the files as most_significant to least
    significant.
    """
    def __init__(self, *config_fn_list):

        self._config_fn_list = [os.path.abspath(fn) for fn in config_fn_list]
        self._config_list = [ConfigurationFile(fn) for fn in self._config_fn_list]

        return

    def sections(self):
        # Python doens't have an OrderedSet so I'm doing the same thing with an OrderedDict.
        section_dict = collections.OrderedDict()
        for section in list(itertools.chain(*[ez.sections() for ez in self._config_list])):
            section_dict[section] = True
        return list(section_dict.keys())

    def get_key_help(self, key, value):
      # Trying this unusual heuristic to get over the fact that the
      # more recent files in rare cases will have better comments; in
      # others the older files.  So we call the longest help the best help.
      ret = sorted([conf.get_key_help(key, value) for conf in self._config_list], key=len)[-1]
      return ret

    def variables(self):
        variable_dict = collections.OrderedDict()
        for section in list(itertools.chain(*[ez.variables() for ez in self._config_list])):
            variable_dict[section] = True
        return list(variable_dict.keys())

    def parse_string(self, *args, **kwds):
        return self._config_list[0].parse_string(*args, **kwds)

    def get(self, *args, **kwds):
        # The only thing here is that we must keep track of
        # mandatory=True.  That makes things a little gross.

        if "default" in kwds and "mandatory" not in kwds:
          kwds["mandatory"] = False

        # Handle mandatory as a special case
        if kwds.get("mandatory", False):
          if not True in [c.has(*args) for c in self._config_list]:
            self._config_list[0].get(*args, mandatory=True)

        section, key = args[:2]
        potential_values = [x for x in [conf.get(*args, **dict(list(kwds.items()) + list({"mandatory": False}.items()))) for conf in self._config_list] if x is not None]

        if potential_values:
            return potential_values[0]
        else:
            return self._config_list[0].get(*args, **kwds) # This will throw if mandatory=True


    def has(sect, key):
        return True in [ez.has(sect, key) for ez in self._config_list]


class ConfiguredApplication(object):

    DEFAULT_LOG_FORMAT = "%(levelname)s %(asctime)-15s %(name)s: %(message)s"

    def __init__(self, arg_parser):
        self.arg_parser = arg_parser # We own this now.

        self.arg_parser.add_argument("config_list", nargs="+")
        (args, opts) = self.arg_parser.parse_known_args([x for x in sys.argv[1:] if x!="--help"])

        # We reverse it so the "little-endian" specification of the shell: default, system, user
        # will be replaced by the "big-endian" specification of function: check user, then system, then default.
        self.config = Configuration(*reversed(args.config_list))

        self._add_arguments()

        self.opts = self.arg_parser.parse_args()
        self._parse_class_options()

    def _add_arguments(self, conf_variables=None):
      if conf_variables == None:
        conf_variables = self.config.variables()

        for (section, key) in conf_variables:
            # The static param indicates that filename variables are
            # to be considered statically typed and identified from
            # the key name, deduced from whether the key name
            # ends with "_file" (one of the default patterns in
            # ezconfig).

            # This buys us the ability to set the absolute path as the
            # default, so the user sees a useful value, as opposed to
            # a potentially relative path in a file the user has no
            # way of knowing.
            config_val = self.config.get(section, key, static=True)
            self.arg_parser.add_argument(self.config_arg_param_arg_name(section, key),
                                         dest=self.config_arg_param_var_name(section, key),
                                         default=config_val,
                                         help = "{} (Default: {})".format(self.config.get_key_help(section, key), config_val))

        # for (section, key) in self.config.variables():
        #     self.arg_parser.add_argument("--{}/{}".format(section, key),
        #                                  default=self.config.get(section, key),
        #                                  help = self.config.get_key_help(section, key))
        return

    def config_arg_param_arg_name(self, section, key):
        return "--{}/{}".format(section, key)

    def config_arg_param_var_name(self, section, key):
        return "{}___{}".format(section, key) # 3 underscores *just in case* someone uses 2 underscores in
                                              # a configuration variable somewhere.


    def get_param_value(self, section, key, **kwds):
        # We capture this value because the configuration has already
        # reported in absolute path the value it holds. So if we get a
        # relative path, it comes from the command line and should be
        # relative to getcwd.

        rawstr = vars(self.opts)[self.config_arg_param_var_name(section, key)]

        if "is_filename" in kwds:
            kwds.pop("is_filename")
            value = self.config.parse_string(rawstr, **kwds)
            value = os.path.abspath(value)
        else:
            value = self.config.parse_string(rawstr, **kwds)

        return value
