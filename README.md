# EZ Config

EZConfig is a package for parsing configuration files.

## Insallation Instructions

Install with pip using

        pip install git+ssh://git@bitbucket.com/nathanaddy/ezconfig.git

## Package Features

EZConfig provides three major features.

* A Configuration class that wraps the system ConfigParser
  class. It exposes the same get/has/sections interface but the
  get method is overloaded to provide many features.

    *  automatic date parsing

    *  time interval parsing (specify ints, floats, or a float/str
       specifier like 12.5m, 3h, 2.5d.

    *  Filename parsing that returns the absolute path of the config
       param relative to the file in which it was specified.

    *  typecasting to python types

    *  specifying a list, so that a list of filenames or dates or any
       other type supported by the library to be returned as a list
       of the correct type.

    *  Features enabling specifying a lambda function in a
       configuration file, allowing easy specification for user
       defined functionality.

* A ConfigurationSet class that takes a set of filenames and
  exposes a Configuration API interface that allows for querying
  the list of Configuration files together using most*significant
  first rules.

* A set of functions for searching for configuration files in
  standard and developer*friendly locations. EZConfig can easily
  be used to check for repo config files, user home directory
  config files, and system config files and either use the
  one*and*only best or as a ConfigurationSet that uses them all
  together, using values from more-significant configuration
  directories.
