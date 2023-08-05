# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['samoyed']

package_data = \
{'': ['*']}

install_requires = \
['ujson>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'samoyed',
    'version': '0.1.0.dev1',
    'description': 'Idiomatic AWS lambda utility specialized for SAM',
    'long_description': '# SAMoyed\nIdiomatic AWS lambda utility specialized for SAM\n\n![](https://www.purina.com.au/-/media/Project/Purina/Main/Breeds/Dog/Dog_Samoyed_Desktop.jpg?h=475&la=en&w=825&hash=141A7757B0B0C4925227669C085DDA69)\n',
    'author': 'Seonghyeon Kim',
    'author_email': 'self@seonghyeon.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NovemberOscar/SAMoyed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
