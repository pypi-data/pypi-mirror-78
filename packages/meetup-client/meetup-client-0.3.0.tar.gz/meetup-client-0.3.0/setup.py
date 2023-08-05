# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meetup', 'meetup.client']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.1,<2.0.0', 'requests>=2.24.0,<3.0.0', 'tqdm>=4.48.2,<5.0.0']

setup_kwargs = {
    'name': 'meetup-client',
    'version': '0.3.0',
    'description': 'A Python client for the Meetup API.',
    'long_description': '# meetup-client\n\n[![Build Status](https://travis-ci.org/janjagusch/meetup-client.svg?branch=master)](https://travis-ci.org/janjagusch/meetup-client) [![codecov](https://codecov.io/gh/janjagusch/meetup-client/branch/master/graph/badge.svg)](https://codecov.io/gh/janjagusch/meetup-client)\n\nA Python client for the [Meetup API](https://www.meetup.com/meetup_api/) that supports [OAuth 2](https://www.meetup.com/meetup_api/auth/#oauth2) authentification.\n\n## Installation\n\n### Dependencies\n\nFor more information, please take a look at the `tool.poetry.dependencies` section in `pyproject.toml`.\n\n### User Installation\n\n#### PIP\n\n```\npip install meetup-client\n```\n\n#### Poetry\n\n```\npoetry add meetup-client\n```\n\n## Getting Started\n\n**Note**: meetup-client only supports OAuth 2 authentification with server flow without user credentials. To create an access token, follow the instructions [here](https://www.meetup.com/meetup_api/auth/#oauth2).\n\nNext, you can create a `MeetupClient` instance as follows:\n\n```python\nfrom meetup_api.client import MeetupClient\n\nmeetup_client = MeetupClient(\n    access_token=<YOUR ACCESS TOKEN>,\n)\n```\n\n## Examples\n\nPlease take a look at the [examples](notebooks/examples.py). You can convert this into a Jupyter notebook, using [jupytext](https://github.com/mwouts/jupytext).\n\n## Changelog\n\nPlease take a look at the [CHANGELOG.md](CHANGELOG.md) for notable changes to meetup-client.\n\n## License\n\nSee the [LICENSE](LICENSE) for details.\n\n## Development\n\nWe welcome new contributions to this project!\n\n### Source Code\n\nYou can check the latest source code with the command:\n\n```\ngit clone git@github.com:janjagusch/meetup-client.git\n```\n\n### Dependencies\n\nPlease take a look at `tool.poetry.dev-dependencies` in `pyproject.toml`.\n\n### Linting\n\nAfter cloning and installing the dependencies, you can lint the project by executing:\n\n```\nmake lint\n```\n\n### Testing\n\nAfter cloning and installing the dependencies, you can test the project by executing:\n\n```\nmake test\n```\n\n## Help and Support\n\n### Authors\n\n- Jan-Benedikt Jagusch <jan.jagusch@gmail.com>\n',
    'author': 'Jan-Benedikt Jagusch',
    'author_email': 'jan.jagusch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/janjagusch/meetup-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
