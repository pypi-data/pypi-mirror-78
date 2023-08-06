# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imageprocessing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'imageprocessing',
    'version': '0.1.1',
    'description': 'This is a package that will allow you to remove the background of any image and replace it with another',
    'long_description': None,
    'author': 'Raviish Panicker',
    'author_email': 'panicker.raviish2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
