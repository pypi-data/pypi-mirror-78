# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_logging', 'flask_logging.handlers']

package_data = \
{'': ['*']}

install_requires = \
['blinker>=1.4,<2.0', 'flask>=1.1.2,<2.0.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'flask-logging-helpers',
    'version': '0.1.2',
    'description': 'Logging tools for flask',
    'long_description': None,
    'author': 'Alex Rudy',
    'author_email': 'opensource@alexrudy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
