# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crf_tagger']

package_data = \
{'': ['*']}

install_requires = \
['python-crfsuite==0.9.7', 'scikit-learn', 'tabulate', 'tqdm']

setup_kwargs = {
    'name': 'crf-tagger',
    'version': '0.3.1',
    'description': 'CRF tagger',
    'long_description': None,
    'author': 'severinsimmler',
    'author_email': 's.simmler@snapaddy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
