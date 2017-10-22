.. Quickstart

Quickstart
--------------

This file describes how one goes about installing and using ezconfig
to solve a variety of common tasks such as searching for configuration
files, looking through multiple configuration files for values, and
parsing configuration values.

If you've spent too much of your life writing too many little parsers
to read configuration strings, this library may help you save
what little time you have left on this planet for more productive
activities.


Installing
=============

EZConfig is installed using pip.

```pip install ezconfig```


Example
=========

The following example gives a quick example of how to use ezconfig to
parse a single Configuration file at a time.

This example uses a configuration file from the project repository referenced in examples/example1.conf

Configuration file:
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python


   [section_one]

   variable = first value # Comments are automatically supported
   names = Tom, Dick, Harry

   float_value = 3.14
   fibonnacci = 1,2,3,4,5

   timedelta_1 = 10
   timedelta_2 = 3.4m

   a_date = 12/30/2017 4:14
   birthdays = 12/30/1975, Mar-30 1981, 1980-10-10

   directory_of_conf_file = .
   user_directory = ~

   adder = lambda x: x+10

EZConfig example
~~~~~~~~~~~~~~~~~~~~

The following code is run loading that configuration.  This shows
several examples of using the major arguments that overload the get
method: default and mandatory, type, is_List, is_timedelta,
is_datetime, and is_filename.

>>> import ezconfig.config

>>> conf = ezconfig.config.Configuration("examples/example1.conf")

>>> print conf.get("section_one", "variable")
first value

>>> print conf.get("section_one", "names", is_list=True)
[u'Tom', u'Dick', u'Harry']

>>> print conf.get("section_one", "float_value", type=float)
3.14

>>> print conf.get("section_one", "float_value", type=float, is_list=True)
[3.14]

>>> print conf.get("section_one", "fibonnacci", type=int, is_list=True)
[1, 2, 3, 4, 5]

>>> print conf.get("section_one", "timedelta_1", is_timedelta=True)
10.0

>>> print conf.get("section_one", "timedelta_2", is_timedelta=True)
204.0

>>> print conf.get("section_one", "a_date", is_datetime=True)
2017-12-30 04:14:00

>>> print conf.get("section_one", "birthdays", is_datetime=True, is_list=True)
[datetime.datetime(1975, 12, 30, 0, 0),
     datetime.datetime(1981, 3, 30, 0, 0),
     datetime.datetime(1980, 10, 10, 0, 0)]

>>> print conf.get("section_one", "directory_of_conf_file", is_filename=True)
/Users/nathan/Source/windfall/ezconfig/examples

>>> print conf.get("section_one", "user_directory", is_filename=True)
/Users/nathan

>>> print conf.get("section_one", "missing_value", default="this is the default")
this is the default

>>> adder_function = conf.get("section_one", "adder", is_code=True)

>>> print adder_function(10)
20
