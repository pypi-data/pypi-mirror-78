# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sa2schema', 'sa2schema.to', 'sa2schema.to.pydantic']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.3.5,<2.0.0']

setup_kwargs = {
    'name': 'sa2schema',
    'version': '0.1.0b3',
    'description': 'Convert SqlAlchemy models to Pydantic',
    'long_description': None,
    'author': 'Mark Vartanyan',
    'author_email': 'kolypto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kolypto/py-sa2schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
