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
    'version': '0.1.1',
    'description': 'A tool to convert sets of Jupyter notebook files into a single, cohesive set of linked pages',
    'long_description': "nbpretty\n========\n\nnbpretty is a tool to convert sets of notebook files into a single, cohesive set of linked pages.\n\nUsage\n-----\n\nCreate a file called ``config.yaml`` with the following contents:\n\n.. code-block:: yaml\n\n   ---\n   course_title: Best practices in software engineering\n\nThe main pages will be created bases on their names.\nYou should name your chapters like: ``00 Introduction.ipynb``, ``01 First Chapter.ipynb`` etc.\n\nand then run it with:\n\n.. code-block:: shell-session\n\n   nbpretty .\n\nIt will write out HTML and CSS files which can then be uploaded/viewed/whatever.\n\nFor development, I recommend using `entr <http://eradman.com/entrproject/>`_ with:\n\n.. code-block:: shell-session\n\n   while sleep 1 ; do find . -name '*.ipynb' | entr -d nbpretty . ; done\n",
    'author': 'Matt Williams',
    'author_email': 'matt@milliams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/milliams/nbpretty',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
