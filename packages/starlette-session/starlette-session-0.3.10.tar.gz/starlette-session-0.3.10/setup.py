# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_session']

package_data = \
{'': ['*']}

install_requires = \
['itsdangerous>=1.1.0,<2.0.0', 'starlette>=0.13.8,<0.14.0']

setup_kwargs = {
    'name': 'starlette-session',
    'version': '0.3.10',
    'description': 'A library for backend side session with starlette',
    'long_description': '<p align="center">\n\n<a href="https://github.com/auredentan/starlette-session/actions?query=workflow%3ATest" target="_blank">\n  <img src="https://github.com/auredentan/starlette-session/workflows/Test/badge.svg?branch=master" alt="Test"/>\n</a>\n\n<a href="https://pypi.org/project/starlette-session" target="_blank">\n  <img src="https://img.shields.io/pypi/v/starlette-session?color=%2334D058&label=pypi%20package" alt="Package version"/>\n</a>\n\n<a href="https://codecov.io/gh/auredentan/starlette-session" target="_blank">\n  <img src="https://codecov.io/gh/auredentan/starlette-session/branch/master/graph/badge.svg" alt="Code coverage"/>\n</a>\n\n</p>\n\n---\n\n**Documentation:** [https://auredentan.github.io/starlette-session/](https://auredentan.github.io/starlette-session/)\n\n---\n\n# Starlette Session\n\nStarlette session is a simple session middleware for [starlette](https://github.com/encode/starlette/). It gives you the possibility of backend session with a predefined backend or a custom one.\n\n## Requirements\n\nPython 3.6+\n\n## Installation\n\n```bash\npip install starlette-session\n```\n',
    'author': 'Aurélien Dentan',
    'author_email': 'aurelien.dentan@gmail.com',
    'maintainer': 'Aurélien Dentan',
    'maintainer_email': 'aurelien.dentan@gmail.com',
    'url': 'https://github.com/auredentan/starlette-sessionhttps://github.com/auredentan/starlette-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
