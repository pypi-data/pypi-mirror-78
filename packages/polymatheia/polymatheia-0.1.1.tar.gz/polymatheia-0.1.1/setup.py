# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['polymatheia', 'polymatheia.data']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.5.2,<5.0.0',
 'munch>=2.5.0,<3.0.0',
 'pandas>=1.1.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'sickle>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'polymatheia',
    'version': '0.1.1',
    'description': 'A python library to support digital archive metadata use',
    'long_description': None,
    'author': 'Mark Hall',
    'author_email': 'mark.hall@work.room3b.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
