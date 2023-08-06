# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minionize']

package_data = \
{'': ['*']}

install_requires = \
['execo>=2.6.4,<3.0.0', 'google-cloud-pubsub>=1.7.0,<2.0.0']

entry_points = \
{'console_scripts': ['minionize = minionize.cli:run']}

setup_kwargs = {
    'name': 'minionize',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'msimonin',
    'author_email': 'matthieu.simonin@inria.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
