# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norwegian_forest_cat']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'norwegian-forest-cat',
    'version': '0.0.4',
    'description': 'A small example package',
    'long_description': None,
    'author': 'chiawei chang',
    'author_email': 'williamcw.chang@moxa.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
