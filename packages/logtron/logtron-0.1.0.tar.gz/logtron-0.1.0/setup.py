# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtron', 'logtron.config', 'logtron.formatters', 'logtron.handlers']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'logtron',
    'version': '0.1.0',
    'description': 'A simple logging library with JSON log formatting',
    'long_description': '# logtron\n',
    'author': 'Ilija Stevcev',
    'author_email': 'ilija1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ilija1/logtron/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
