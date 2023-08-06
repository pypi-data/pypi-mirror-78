# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apywrapper']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.5.1,<2.0.0', 'httpx>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'apywrapper',
    'version': '0.1.8',
    'description': 'make wrapper for RESTful API',
    'long_description': '## apywrapper\n\n![lint](https://github.com/sh1ma/apywrapper/workflows/lint/badge.svg?branch=develop)\n[![PyPI version](https://badge.fury.io/py/apywrapper.svg)](https://badge.fury.io/py/apywrapper)\n\nEasy development of RESTful API wrapper\n\n## Feature\n- Get response as dataclass object you defined\n- Return type can be specified by type annotation of api function\n- All parameters (query, path variable, or json data) can be specified at once\n\n\n## install\n\n```\npip install apywrapper\n```\n\n## Example\n\n```python\nfrom apywrapper import Apy, delete, get, patch, post, put\nfrom typing import List, no_type_check\nfrom dataclasses import dataclass\n\n\n@dataclass\nclass User:\n    name: str\n    id: str\n\n\n@no_type_check\nclass ApiClient(Apy):\n    def __init__(self, token, host="https://example.com/api":\n        super().__init__(host, headers={"api-token": token})\n\n    @get("/users/")\n    def get_users(self) -> List[User]:\n        return {}\n\n    @get("/users/{user_id}")\n    def get_user(self, user_id) -> User:\n        return {"user_id": user_id}\n\napi = ApiClient(token="xxxxxxxxxxxxxxxxxx")\nsh1ma = api.get_user("sh1ma") # return User object\n```',
    'author': 'sh1ma',
    'author_email': 'in9lude@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sh1ma/apywrapper',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
