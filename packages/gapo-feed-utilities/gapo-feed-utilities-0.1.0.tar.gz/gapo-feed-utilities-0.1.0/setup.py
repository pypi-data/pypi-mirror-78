# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gapo_feed_utilities']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'pydantic>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['poetry = poetry.console:run']}

setup_kwargs = {
    'name': 'gapo-feed-utilities',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'nguyentrongphan@gapo.com.vn',
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
