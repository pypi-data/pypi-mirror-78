# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbg', 'nbg.auth', 'nbg.base']

package_data = \
{'': ['*'], 'nbg.auth': ['certs/*']}

install_requires = \
['python-jose[cryptography]>=3.1.0,<4.0.0', 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'nbg',
    'version': '0.6.0',
    'description': 'Official Python SDK for NBG APIs',
    'long_description': '# NBG Python SDK\n\n[![Downloads of nbg on PyPI](https://pepy.tech/badge/nbg)](https://pepy.tech/project/nbg) [![nbg is packaged as wheel](https://img.shields.io/pypi/wheel/nbg.svg)](https://pypi.org/project/nbg/) [![Supported Python versions of nbg](https://img.shields.io/pypi/pyversions/nbg.svg)](https://pypi.org/project/nbg/)\n\nThe `nbg <https://pypi.org/project/nbg>`_ Python package enables developers to build applications that use the public APIs of the National Bank of Greece.\n\n\n## Installation\n\nWe suggest using a package manager like [Poetry](https://python-poetry.org) or [Pipenv](https://pipenv.pypa.io) to install `nbg`. This guarantees that the intended version of `nbg` will be installed every time, through content hash checks:\n\n```console\npoetry add nbg\n```\n\nAlternatively you can use Pipenv:\n\n```console\npipenv install nbg\n```\n\nIn case you cannot use Poetry or Pipenv, you can always install `nbg` with [pip](https://pip.pypa.io/en/stable/):\n\n```console\npip install nbg\n```\n\n## API clients\n\nThe National Bank of Greece provides a set of multiple APIs. To use each one of these APIs, you should pick the corresponding client from the `nbg` package.\n\n### Accounts Information PSD2 API\n\n```python\nfrom nbg import account_information\n\n\n# Step 1 - Set up client and authentication\nclient_id="your_client_id"\nclient_secret="your_client_secret"\nclient = account_information.AccountInformationPSD2Client(\n    client_id=client_id,\n    client_secret=client_secret,\n    production=False,\n)\nclient.set_access_token("access_token_of_your_user")\n\n# Step 2 - Set up a sandbox, when in development\nsandbox_id = f"{client_id}_sandbox"\nclient.create_sandbox(sandbox_id)\nclient.set_sandbox(sandbox_id)\n\n# Step 3 - Start working with the Account information API\n\n## Account resource\naccounts = client.accounts(user_id="your_user_id")\nprint(accounts)\n```\n',
    'author': 'Paris Kasidiaris',
    'author_email': 'paris@sourcelair.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
