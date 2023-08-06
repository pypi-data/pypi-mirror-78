# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbpretty']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0', 'nbconvert>=5.6,<6.0']

entry_points = \
{'console_scripts': ['nbpretty = nbpretty:main']}

setup_kwargs = {
    'name': 'nbpretty',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Matt Williams',
    'author_email': 'matt@milliams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
