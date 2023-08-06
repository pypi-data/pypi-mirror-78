# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niva_api_client', 'niva_api_client.domain', 'niva_api_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['poetry-version>=0.1.5,<0.2.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests==2.24.0',
 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'niva-api-client',
    'version': '0.1.0',
    'description': "Client library for interacting with API's exposed at https://data.niva.no. Handles common tasks such as authentication",
    'long_description': None,
    'author': 'Håkon Drolsum Røkenes',
    'author_email': 'hakon.rokenes@niva.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
