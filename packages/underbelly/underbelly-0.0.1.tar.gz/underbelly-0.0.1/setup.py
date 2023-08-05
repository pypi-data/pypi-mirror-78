# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['underbelly',
 'underbelly.envs',
 'underbelly.envs.models',
 'underbelly.envs.modules',
 'underbelly.envs.modules.db',
 'underbelly.envs.modules.episodes',
 'underbelly.envs.modules.metrics',
 'underbelly.envs.modules.opts',
 'underbelly.envs.modules.schemas',
 'underbelly.envs.utils',
 'underbelly.orders',
 'underbelly.orders.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0',
 'networkx>=2.5,<3.0',
 'pydantic>=1.6.1,<2.0.0',
 'pytest-sugar>=0.9.4,<0.10.0',
 'pytest>=6.0.1,<7.0.0',
 'redistimeseries>=0.8.0,<0.9.0',
 'scipy>=1.5.2,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'toolz>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'underbelly',
    'version': '0.0.1',
    'description': 'The rust underpinnings to the Jamboree library.',
    'long_description': None,
    'author': 'karamel',
    'author_email': 'kivo360@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
