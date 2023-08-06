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
    'version': '0.1.4',
    'description': 'make wrapper for RESTful API',
    'long_description': '## apywrapper\n\nEasy development of RESTful API wrapper\n\n\n## install\n\n```\npip install apywrapper\n```\n\n\n## Example (Chatwork API Wrapper)\n\n```python\nfrom apywrapper import Apy\nfrom dataclasses import dataclass\n\napi = Apy(\n    "https://api.chatwork.com/v2",\n    headers={"X-ChatWorkToken": "xxxxxxxxx"},\n)\n\n\n@dataclass\nclass Room:\n    room_id: int\n    name: str\n    type: str\n    role: str\n    sticky: bool\n    unread_num: int\n    mention_num: int\n    mytask_num: int\n    message_num: int\n    file_num: int\n    task_num: int\n    icon_path: str\n    last_update_time: int\n\n\n@api.get("/rooms/{room_id}")\ndef get_room(room_id: int):\n    return (\n        Room,\n        {"room_id": room_id},\n    )  # Return Object, Request Params(Path Args, Query or JsonData(Dict))\n\n\n@api.get("/rooms")\ndef get_rooms():\n    return Room, {}\n\n\nprint(get_room(113377551))  # return Room\nprint(get_rooms()) # return List[Room]\n\n```\n\n## Example (POST data)\n```python\n@api.post("/users")\ndef create_user(username: str, user_id: str):\n    return User, {"user_name": username, "user_id": user_id}\n\ncreated_user = create_user("sh1ma", "sh1ma")\n```\n\n## Example (GET with `is_hello` query)\n```python\n@api.get("/users/{user_id}")\ndef get_user(user_id: str, is_hello: bool):\n    return User, {"user_id": user_id, "is_hello": True}\n```\n\n',
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
