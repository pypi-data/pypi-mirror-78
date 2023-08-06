# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['purepress']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0',
 'Markdown>=3.2.2,<4.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'Werkzeug>=1.0.1,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'feedgen>=0.9.0,<0.10.0',
 'py-gfm>=1.0.0,<2.0.0',
 'pytz>=2020.1,<2021.0']

entry_points = \
{'console_scripts': ['purepress = purepress.cli:main']}

setup_kwargs = {
    'name': 'purepress',
    'version': '0.1.0',
    'description': 'A simple static blog generator.',
    'long_description': '# PurePress\n\n**PurePress** is a very simple static blog generator.\n',
    'author': 'Richard Chien',
    'author_email': 'richardchienthebest@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richardchien/purepress',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
