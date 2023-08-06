# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pddl2gym']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pddl2gym',
    'version': '0.0.1',
    'description': 'A translator from PDDL domain/problem files to OpenAI Gym environment.',
    'long_description': None,
    'author': 'MarcoFavorito',
    'author_email': 'marco.favorito@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
