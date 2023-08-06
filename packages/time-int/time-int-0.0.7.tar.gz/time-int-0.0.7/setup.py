# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_int']

package_data = \
{'': ['*']}

install_requires = \
['magic-kind>=0.2.2,<0.3.0', 'pytest>=5.4.2,<6.0.0']

setup_kwargs = {
    'name': 'time-int',
    'version': '0.0.7',
    'description': 'Subclass of integer representing seconds since UNIX epoch',
    'long_description': '# time-int\nInteger subclass to represent naive time since epoch.\n\n### The Idea\nUNIX has a venerable tradition of representing time as seconds since the\nstart of 1970. This has its limitations, but it is sometimes desirably\nsimple. This package sub-classes int to give a little handy functionality\nto this simple approach.\n\n### Important Limitations\n* Supported range starts at 0 or TimeInt.MIN on Jan 1, 1970\n* Supported range ends at a 32-bit limit or TimeInt.MAX on Apr 2, 2106\n* Values are rounded off to the nearest second.\n* Values do not track what time-zone they represent.\n\n### Quick Example\n```python\nfrom time_int import TimeInt\n\nstart_time = TimeInt.utcnow()\nsome_slow_operation()\nend_time = TimeInt.utcnow()\n\nprint(f"Operation started at {start_time.get_pretty()}")\nprint(f"Operation ended  at  {end_time.get_pretty()}")\nprint(f"Operation took {end_time - start_time} seconds")\n```\n\n### The trunc_\\<unit\\> Methods\nSome trunc_\\<unit\\> methods are available for rounding down times to the\nyear, month, week, day, hour, or minute. One can also round down to units based\non some number of these units. For example to round a time int to the fifteen\nminute period it falls in:\n```python\nfrom time_int import TimeInt\nfrom datetime import datetime\n\ndt = datetime(year=2001, month=5, day=16, hour=10, minute=53)\ntime = TimeInt.from_datetime(dt)\n\nquarter_hour_time = time.trunc_minute(num=15)\n``` \nThe `quater_hour_time` will round down 10:53am to 10:45am.\nNote that the 15 minute periods rounded to are based on when the hour started, as\none might intuitively suspect. For numbers of hours the `trunc_day` method is based\non start of the day. Such that if you round down to units of 6 hours, you will round\ndown to ether midnight, 6am, noon, or 6pm. Weeks do not have this grouping feature because\nthere is no obvious place I can see to start counting groups of weeks from. For\ndays they are based on start of month. For months on start of year, and for years\non a fictional year 0 (which technically does not exist). Sometimes there will be\noddly sized groups with less than the number of units, for example if you choose to\nround to units of 7 hours, you will get either midnight, 7am, 2pm, or 9pm. With 9pm\nto midnight only being the left over 3 hours. When the time unit is groups of 2 or\nmore days, this is bound to happen due to the way months vary from 28 to 31 days.\n\n##### trunc method\nThere is a generic `trunc` method that wraps all the `trunc_<unit>` methods so\none can specify the basic time unit as an argument. For example to find the start\nof the start of the current quarter year in UTC:\n\n```python\nfrom time_int import TimeInt, TimeTruncUnit\n\ncurrent_time = TimeInt.utcnow()\nstart_of_quarter = current_time.trunc(TimeTruncUnit.MONTH, num=3)\n```\nOf course in this example one would probably just use `trunc_month(num=3)` which\ndoes the same thing.\n\n\n\n\n',
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aallaire/time-int',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
