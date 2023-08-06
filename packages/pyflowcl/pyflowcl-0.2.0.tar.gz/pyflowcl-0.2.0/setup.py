# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyflowcl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pyflowcl',
    'version': '0.2.0',
    'description': 'Cliente para comunicacion con flowAPI-3 de flow.cl',
    'long_description': 'PyFlowCL\n============\n\nCliente API para operaciones con el servicio de pagos Flow.cl  \n[FlowAPI-3.0.1](https://www.flow.cl/docs/api.html) \n\n---\n\n## Features\n- Currently the "[Payment](https://www.flow.cl/docs/api.html#tag/payment)" command is available\n\n\n---\n\n## Setup\nThis project is managed by Poetry (a requierements.txt file is also provided)\n\n---\n\n## Usage\n```python\nfrom pyflowcl import Payment\nfrom pyflowcl.Clients import ApiClient\n\nAPI_URL = "https://sandbox.flow.cl/api"\nAPI_KEY = "your_key"\nAPI_SECRET = "your_secret"\nFLOW_TOKEN = "your_payment_token"\napi = ApiClient(API_URL, API_KEY, API_SECRET)\n\ncall = Payment.get_status(api, FLOW_TOKEN)\nprint(call)\n```\n\n---\n\n## License\n>You can check out the full license [here](https://github.com/mariofix/pyflowcl/blob/stable-v3/LICENSE)\n\nThis project is licensed under the terms of the **MIT** license.  \nFlowAPI is licensed under the terms of the **Apache 2.0** license.\n',
    'author': 'Mario Hernandez',
    'author_email': 'yo@mariofix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mariofix/pyflowcl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
