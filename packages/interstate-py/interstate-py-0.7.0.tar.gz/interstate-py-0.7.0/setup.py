# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interstate_py',
 'interstate_py.control',
 'interstate_py.error',
 'interstate_py.internalio',
 'interstate_py.reactive',
 'interstate_py.serialization',
 'interstate_py.zeromq']

package_data = \
{'': ['*']}

install_requires = \
['aiozmq>=0.7.1,<0.8.0',
 'async_generator>=1.10,<2.0',
 'pyzmq>=18.0,<19.0',
 'rx==1.6.1']

entry_points = \
{'console_scripts': ['build = poetry_scripts:build',
                     'install = poetry_scripts:install',
                     'publish = poetry_scripts:publish',
                     'release = poetry_scripts:release',
                     'test = poetry_scripts:test']}

setup_kwargs = {
    'name': 'interstate-py',
    'version': '0.7.0',
    'description': '',
    'long_description': None,
    'author': 'LeftshiftOne Software GmbH',
    'author_email': 'devs@leftshift.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
