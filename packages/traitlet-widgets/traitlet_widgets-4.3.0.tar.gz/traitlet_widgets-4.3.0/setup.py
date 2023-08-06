# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['traitlet_widgets']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.5,<8.0', 'traitlets>=4.3,<5.0']

setup_kwargs = {
    'name': 'traitlet-widgets',
    'version': '4.3.0',
    'description': 'A library which provides the ability to create widget views for traitlet `HasTraits` models, and also to observe changes in a model',
    'long_description': None,
    'author': 'Angus Hollands',
    'author_email': 'goosey15@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agoose77/traitlet_widgets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
