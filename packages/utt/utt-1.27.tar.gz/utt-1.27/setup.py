# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utt',
 'utt.api',
 'utt.api._v1',
 'utt.components',
 'utt.components.report_model',
 'utt.data_structures',
 'utt.plugins',
 'utt.report',
 'utt.report.activities',
 'utt.report.details',
 'utt.report.per_day',
 'utt.report.projects',
 'utt.report.summary']

package_data = \
{'': ['*']}

install_requires = \
['argcomplete==1.11.1',
 'cargo==0.3',
 'python_dateutil==2.8.1',
 'pytz>=2020,<2021',
 'tzlocal==2.0.0']

entry_points = \
{'console_scripts': ['utt = utt.__main__:main']}

setup_kwargs = {
    'name': 'utt',
    'version': '1.27',
    'description': 'A simple command-line time tracker',
    'long_description': None,
    'author': 'Mathieu Larose',
    'author_email': 'mathieu@mathieularose.com',
    'maintainer': 'Mathieu Larose',
    'maintainer_email': 'mathieu@mathieularose.com',
    'url': 'https://github.com/larose/utt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
