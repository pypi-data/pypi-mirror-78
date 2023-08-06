# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_notebook']

package_data = \
{'': ['*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'numba>=0.51.2,<0.52.0',
 'numpy>=1.19.1,<2.0.0',
 'pandas>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'poetry-notebook',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jean-Christophe Cazes',
    'author_email': 'jean-christophe.cazes@groupeseloger.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
