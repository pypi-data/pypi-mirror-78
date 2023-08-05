# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcs_kfold']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.1,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'mcs-kfold',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Masashi Sode',
    'author_email': 'masashi.sode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
