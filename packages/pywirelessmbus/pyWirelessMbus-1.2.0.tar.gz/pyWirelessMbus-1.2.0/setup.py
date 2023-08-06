# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywirelessmbus',
 'pywirelessmbus.devices',
 'pywirelessmbus.exceptions',
 'pywirelessmbus.sticks',
 'pywirelessmbus.utils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.1,<0.6.0', 'pyserial-asyncio>=0.4,<0.5', 'pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'pywirelessmbus',
    'version': '1.2.0',
    'description': 'A tool to receive and send Wireless-M-Bus messages.',
    'long_description': None,
    'author': 'Karl Wolffgang',
    'author_email': 'karl_eugen.wolffgang@tu-dresden.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gewv-tu-dresden/pyWirelessMbus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
