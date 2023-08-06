# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aio_zmq_rpc']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.0,<2.0.0', 'zmq>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'aio-zmq-rpc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alexander Titoff',
    'author_email': 'a.tit.off@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
